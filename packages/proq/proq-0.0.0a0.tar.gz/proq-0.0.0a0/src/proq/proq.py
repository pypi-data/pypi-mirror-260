from __future__ import annotations

import multiprocessing as mp
from typing import Generic, Iterable, Optional, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class ProqQueue(Generic[T]):
    _END_SENTINEL = ()

    def __init__(self, q: mp.Queue | None = None):
        self._q = q or mp.Queue()
        self._closed = False

    def put(self, item: T):
        assert not self._closed, "ProqQueue is closed."
        self._q.put(item)

    def get(self) -> T:
        return self._q.get()

    def close(self):
        assert not self._closed, "ProqQueue is closed."
        self._q.put(self._END_SENTINEL)

    def collect(self) -> Iterable[T]:
        return list(self.collect_iter())

    def collect_iter(self) -> Iterable[T]:
        while (item := self._q.get()) is not self._END_SENTINEL:
            yield item


class ProqPool(Generic[T, U]):
    def __init__(self, pool: mp.Pool | None = None):
        self._pool = pool or mp.Pool()


class Proq(Generic[T]):
    def __init__(self, q: mp.Queue | None = None, pool: mp.Pool | None = None):
        self._q = q or mp.Queue()
        self._pool = pool | mp.Pool()


def create(iterable: Iterable[T]) -> Proq[T]:
    proq_queue = ProqQueue()
    for item in iterable:
        proq_queue.put(item)
    proq_queue.close()
    return proq_queue


class MagicRegex:
    def __init__(self, text: str):
        self._text = text
        self._regex = None

    @property
    def text(self) -> str:
        return self._text

    @property
    def regex(self) -> re.Pattern:
        if self._regex is None:
            self._regex = re.compile(self._text, re.DOTALL)
        return self._regex

    # Match

    def find(self, text: str) -> Optional[re.Match[str]]:
        return self.regex.search(text)

    def find_all(self, text: str) -> Iterable[re.Match[str]]:
        return self.regex.finditer(text)

    # Split

    def split(self, text: str, maxsplit: int = 0) -> list[str]:
        return self.regex.split(text, maxsplit)

    # Repeat

    def repeat(self, n: int) -> MagicRegex:
        return MagicRegex(f"{self._grouped_text}{{{n}}}")

    def repeat_zero_or_more(self) -> MagicRegex:
        return MagicRegex(f"{self._grouped_text}*")

    def repeat_one_or_more(self) -> MagicRegex:
        return MagicRegex(f"{self._grouped_text}+")

    def optional(self) -> MagicRegex:
        return MagicRegex(f"{self._grouped_text}?")

    # Group

    def group_as(self, name: str) -> MagicRegex:
        return MagicRegex(f"(?P<{name}>{self._text})")

    group = group_as

    # Concat

    def or_(self, other: str | MagicRegex) -> MagicRegex:
        return any_of([self, other])

    def and_(self, other: str | MagicRegex) -> MagicRegex:
        return concat([self, other])

    # Internal functionality

    @property
    def _grouped_text(self) -> str:
        return f"(?:{self.text})"


def exactly(text: str) -> MagicRegex:
    escaped_text = re.escape(text)
    return MagicRegex(escaped_text)


def char_in(chars: str) -> MagicRegex:
    escaped_chars = re.escape(chars)
    return MagicRegex(f"[{escaped_chars}]")


def char_not_in(chars: str) -> MagicRegex:
    escaped_chars = re.escape(chars)
    return MagicRegex(f"[^{escaped_chars}]")


def any_of(items: list[str | MagicRegex]) -> MagicRegex:
    mrex_objects = [
        option if isinstance(option, MagicRegex) else exactly(option)
        for option in items
    ]
    any_of_str = "|".join([obj._grouped_text for obj in mrex_objects])
    return MagicRegex(any_of_str)


def concat(items: list[str | MagicRegex]) -> MagicRegex:
    mrex_objects = [
        option if isinstance(option, MagicRegex) else exactly(option)
        for option in items
    ]
    concatenated_str = "".join([obj._grouped_text for obj in mrex_objects])
    return MagicRegex(concatenated_str)
