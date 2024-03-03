from __future__ import annotations

import datetime as dt
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from os import chdir
from os import walk as _walk
from pathlib import Path

from utilities.datetime import UTC
from utilities.re import extract_group
from utilities.types import PathLike

PWD = Path.cwd()


def ensure_path(
    *parts: PathLike, validate: bool = False, sanitize: bool = False
) -> Path:
    """Ensure a path-like object is a path."""
    if validate or sanitize:
        from utilities.pathvalidate import valid_path

        return valid_path(*parts, sanitize=sanitize)
    return Path(*parts)


def ensure_suffix(path: PathLike, suffix: str, /) -> Path:
    """Ensure a path has the required suffix."""
    path = Path(path)
    parts = path.name.split(".")
    clean_suffix = extract_group(r"^\.(\w+)$", suffix)
    if parts[-1] != clean_suffix:
        parts.append(clean_suffix)
    return path.with_name(".".join(parts))


def get_modified_time(path: PathLike, /) -> dt.datetime:
    """Get the modified time of a file."""
    return dt.datetime.fromtimestamp(Path(path).stat().st_mtime, tz=UTC)


@contextmanager
def temp_cwd(path: PathLike, /) -> Iterator[None]:
    """Context manager with temporary current working directory set."""
    prev = Path.cwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(prev)


def walk(
    top: PathLike,
    /,
    *,
    topdown: bool = True,
    onerror: Callable[[OSError], None] | None = None,
    followlinks: bool = False,
) -> Iterator[tuple[Path, list[Path], list[Path]]]:
    """Iterate through a directory recursively."""
    for dirpath, dirnames, filenames in _walk(
        top, topdown=topdown, onerror=onerror, followlinks=followlinks
    ):
        yield (Path(dirpath), list(map(Path, dirnames)), list(map(Path, filenames)))


__all__ = ["ensure_path", "ensure_suffix", "get_modified_time", "temp_cwd", "walk"]
