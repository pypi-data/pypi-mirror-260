"""Functions to clean cache database and files."""

# Copyright 2022, European Union.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import collections
import datetime
import functools
import json
import posixpath
from typing import Any, Callable, Literal, Optional

import pydantic
import sqlalchemy as sa
import sqlalchemy.orm

from . import config, database, decode, encode, extra_encoders, utils


def _delete_cache_file(
    obj: dict[str, Any],
    session: sa.orm.Session | None = None,
    cache_entry_id: int | None = None,
    sizes: dict[str, int] | None = None,
    dry_run: bool = False,
) -> Any:
    logger = config.get().logger

    if {"type", "callable", "args", "kwargs"} == set(obj) and obj["callable"] in (
        "cacholote.extra_encoders:decode_xr_dataarray",
        "cacholote.extra_encoders:decode_xr_dataset",
        "cacholote.extra_encoders:decode_io_object",
    ):
        sizes = sizes or {}
        cache_fs, cache_dirname = utils.get_cache_files_fs_dirname()
        cache_dirname = cache_fs.unstrip_protocol(cache_dirname)

        fs, urlpath = extra_encoders._get_fs_and_urlpath(*obj["args"][:2])
        urlpath = fs.unstrip_protocol(urlpath)

        if posixpath.dirname(urlpath) == cache_dirname:
            size = sizes.pop(urlpath, 0)
            if not dry_run:
                if session:
                    for cache_entry in session.scalars(
                        sa.select(database.CacheEntry).filter(
                            database.CacheEntry.id == cache_entry_id
                        )
                    ):
                        logger.info("delete cache entry", cache_entry=cache_entry)
                        session.delete(cache_entry)
                    database._commit_or_rollback(session)

                if fs.exists(urlpath):
                    logger.info("delete cache file", urlpath=urlpath, size=size)
                    fs.rm(
                        urlpath,
                        recursive=obj["args"][0]["type"] == "application/vnd+zarr",
                    )

    return obj


def _delete_cache_entry(
    session: sa.orm.Session, cache_entry: database.CacheEntry
) -> None:
    # First, delete database entry
    session.delete(cache_entry)
    database._commit_or_rollback(session)
    # Then, delete files
    json.loads(cache_entry._result_as_string, object_hook=_delete_cache_file)


def delete(func_to_del: str | Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    """Delete function previously cached.

    Parameters
    ----------
    func_to_del: callable, str
        Function to delete from cache
    *args: Any
        Argument of functions to delete from cache
    **kwargs: Any
        Keyword arguments of functions to delete from cache
    """
    hexdigest = encode._hexdigestify_python_call(func_to_del, *args, **kwargs)
    with config.get().instantiated_sessionmaker() as session:
        for cache_entry in session.scalars(
            sa.select(database.CacheEntry).filter(database.CacheEntry.key == hexdigest)
        ):
            _delete_cache_entry(session, cache_entry)


class _Cleaner:
    def __init__(self) -> None:
        self.logger = config.get().logger
        self.fs, self.dirname = utils.get_cache_files_fs_dirname()

        urldir = self.fs.unstrip_protocol(self.dirname)

        self.logger.info("get disk usage of cache files")
        self.sizes: dict[str, int] = collections.defaultdict(int)
        for path, size in self.fs.du(self.dirname, total=False).items():
            # Group dirs
            urlpath = self.fs.unstrip_protocol(path)
            basename, *_ = urlpath.replace(urldir, "", 1).strip("/").split("/")
            if basename:
                self.sizes[posixpath.join(urldir, basename)] += size

    @property
    def size(self) -> int:
        sum_sizes = sum(self.sizes.values())
        self.logger.info("check cache files total size", size=sum_sizes)
        return sum_sizes

    def stop_cleaning(self, maxsize: int) -> bool:
        return self.size <= maxsize

    def get_unknown_files(self, lock_validity_period: float | None) -> set[str]:
        self.logger.info("get unknown files")

        utcnow = utils.utcnow()
        files_to_skip = []
        for urlpath in self.sizes:
            if urlpath.endswith(".lock"):
                modified = self.fs.modified(urlpath)
                if modified.tzinfo is None:
                    modified = modified.replace(tzinfo=datetime.timezone.utc)
                delta = utcnow - modified
                if lock_validity_period is None or delta < datetime.timedelta(
                    seconds=lock_validity_period
                ):
                    files_to_skip.append(urlpath)
                    files_to_skip.append(urlpath.rsplit(".lock", 1)[0])

        unknown_sizes = {k: v for k, v in self.sizes.items() if k not in files_to_skip}
        if unknown_sizes:
            with config.get().instantiated_sessionmaker() as session:
                for cache_entry in session.scalars(sa.select(database.CacheEntry)):
                    json.loads(
                        cache_entry._result_as_string,
                        object_hook=functools.partial(
                            _delete_cache_file,
                            sizes=unknown_sizes,
                            dry_run=True,
                        ),
                    )
        return set(unknown_sizes)

    def delete_unknown_files(
        self, lock_validity_period: float | None, recursive: bool
    ) -> None:
        for urlpath in self.get_unknown_files(lock_validity_period):
            size = self.sizes.pop(urlpath)
            if self.fs.exists(urlpath):
                self.logger.info(
                    "delete unknown", urlpath=urlpath, size=size, recursive=recursive
                )
                self.fs.rm(urlpath, recursive=recursive)

    @staticmethod
    @pydantic.validate_call
    def _get_tag_filters(
        tags_to_clean: Optional[list[Optional[str]]],
        tags_to_keep: Optional[list[Optional[str]]],
    ) -> list[sa.ColumnElement[bool]]:
        if (tags_to_clean is not None) and (tags_to_keep is not None):
            raise ValueError("tags_to_clean/keep are mutually exclusive.")

        filters = []
        if tags_to_keep is not None:
            filters.append(
                sa.or_(
                    database.CacheEntry.tag.not_in(tags_to_keep),
                    database.CacheEntry.tag.is_not(None)
                    if None in tags_to_keep
                    else database.CacheEntry.tag.is_(None),
                )
            )
        elif tags_to_clean is not None:
            filters.append(
                sa.or_(
                    database.CacheEntry.tag.in_(tags_to_clean),
                    database.CacheEntry.tag.is_(None)
                    if None in tags_to_clean
                    else database.CacheEntry.tag.is_not(None),
                )
            )
        return filters

    @staticmethod
    @pydantic.validate_call
    def _get_method_sorters(
        method: Literal["LRU", "LFU"],
    ) -> list[sa.orm.InstrumentedAttribute[Any]]:
        sorters: list[sa.orm.InstrumentedAttribute[Any]] = []
        if method == "LRU":
            sorters.extend([database.CacheEntry.timestamp, database.CacheEntry.counter])
        elif method == "LFU":
            sorters.extend([database.CacheEntry.counter, database.CacheEntry.timestamp])
        else:
            raise ValueError(f"{method=}")
        sorters.append(database.CacheEntry.expiration)
        return sorters

    def delete_cache_files(
        self,
        maxsize: int,
        method: Literal["LRU", "LFU"],
        tags_to_clean: list[str | None] | None,
        tags_to_keep: list[str | None] | None,
    ) -> None:
        filters = self._get_tag_filters(tags_to_clean, tags_to_keep)
        sorters = self._get_method_sorters(method)

        if self.stop_cleaning(maxsize):
            return
        start_timestamp = utils.utcnow()

        # Get entries to clean
        with config.get().instantiated_sessionmaker() as session:
            cache_entry_ids = session.scalars(
                sa.select(database.CacheEntry.id).filter(*filters).order_by(*sorters)
            )

        # Loop over entries
        for cache_entry_id in cache_entry_ids:
            with config.get().instantiated_sessionmaker() as session:
                filters = [
                    database.CacheEntry.id == cache_entry_id,
                    # skip entries updated while cleaning
                    database.CacheEntry.timestamp < start_timestamp,
                ]
                for cache_entry in session.scalars(
                    sa.select(database.CacheEntry).filter(*filters)
                ):
                    json.loads(
                        cache_entry._result_as_string,
                        object_hook=functools.partial(
                            _delete_cache_file,
                            session=session,
                            cache_entry_id=cache_entry.id,
                            sizes=self.sizes,
                        ),
                    )
                    if self.stop_cleaning(maxsize):
                        return

        raise ValueError(
            f"Unable to clean {self.dirname!r}. Final size: {self.size!r}. Expected size: {maxsize!r}"
        )


def clean_cache_files(
    maxsize: int,
    method: Literal["LRU", "LFU"] = "LRU",
    delete_unknown_files: bool = False,
    recursive: bool = False,
    lock_validity_period: float | None = None,
    tags_to_clean: list[str | None] | None = None,
    tags_to_keep: list[str | None] | None = None,
) -> None:
    """Clean cache files.

    Parameters
    ----------
    maxsize: int
        Maximum total size of cache files (bytes).
    method: str, default: "LRU"
        * LRU: Last Recently Used
        * LFU: Least Frequently Used
    delete_unknown_files: bool, default: False
        Delete all files that are not registered in the cache database.
    recursive: bool, default: False
        Whether to delete unknown directories or not
    lock_validity_period: float, optional, default: None
        Validity period of lock files in seconds. Expired locks will be deleted.
    tags_to_clean, tags_to_keep: list of strings/None, optional, default: None
        Tags to clean/keep. If None, delete all cache entries.
        To delete/keep untagged entries, add None in the list (e.g., [None, 'tag1', ...]).
        tags_to_clean and tags_to_keep are mutually exclusive.
    """
    cleaner = _Cleaner()

    if delete_unknown_files:
        cleaner.delete_unknown_files(lock_validity_period, recursive)

    cleaner.delete_cache_files(
        maxsize=maxsize,
        method=method,
        tags_to_clean=tags_to_clean,
        tags_to_keep=tags_to_keep,
    )


def clean_invalid_cache_entries(
    check_expiration: bool = True, try_decode: bool = False
) -> None:
    """Clean invalid cache entries.

    Parameters
    ----------
    check_expiration: bool
        Whether or not to delete expired entries
    try_decode: bool
        Whether or not to delete entries that raise DecodeError (this can be slow!)
    """
    filters = []
    if check_expiration:
        filters.append(database.CacheEntry.expiration <= utils.utcnow())
    if filters:
        with config.get().instantiated_sessionmaker() as session:
            for cache_entry in session.scalars(
                sa.select(database.CacheEntry).filter(*filters)
            ):
                _delete_cache_entry(session, cache_entry)

    if try_decode:
        with config.get().instantiated_sessionmaker() as session:
            for cache_entry in session.scalars(sa.select(database.CacheEntry)):
                try:
                    decode.loads(cache_entry._result_as_string)
                except decode.DecodeError:
                    _delete_cache_entry(session, cache_entry)
