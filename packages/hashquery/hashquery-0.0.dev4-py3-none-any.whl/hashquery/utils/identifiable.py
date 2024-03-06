from typing import *
from dataclasses import dataclass, field
from typing import Any


class Identifiable(Protocol):
    identifier: str


T = TypeVar("T", bound=Identifiable)


class IdentifiableMap(Generic[T]):
    """
    A dict-like structure which collects a list of values
    keyed against their `.identifier` property.
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        super().__init__()
        # using a dict would be faster, but keeping the keys and the value's
        # identifiers in sync could be hard -- boxing items into a `set` is
        # probably the best approach here, but leaving it simple for now
        self.storage: List[T] = list(items) if items else []

    def add(self, value: T) -> None:
        existing_idx, _ = self._id_access(value.identifier)
        if existing_idx is not None:
            self.storage[existing_idx] = value
        else:
            self.storage.append(value)

    def remove(self, value: T) -> None:
        idx, _ = self._id_access(value.identifier)
        if not idx:
            raise KeyError(value.identifier)
        self.storage.pop(idx)

    def get(self, key: str, default=None) -> Optional[T]:
        idx, item = self._id_access(key)
        if idx is None:
            return default
        else:
            return item

    def _id_access(self, identifier: str, error=None) -> T:
        for idx, item in enumerate(self.storage):
            if item.identifier == identifier:
                return idx, item
        if error:
            raise error
        return None, None

    def __getitem__(self, key: str) -> T:
        _, item = self._id_access(key, error=KeyError(key))
        return item

    def __len__(self):
        return len(self.storage)

    def __iter__(self) -> Iterator[T]:
        return self.storage.__iter__()
