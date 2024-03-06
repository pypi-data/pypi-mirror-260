from typing import *

W = TypeVar("W")
T = TypeVar("T")


class AccessProxy(Generic[W, T]):
    """
    Proxies access into the provided collection with dot or subscript,
    without exposing the collection itself. The collection must support
    `.__getitem__(key)`, and only those attributes will be exposed.

    `transformer` can be applied to transform accessed values before they
    exit the proxy to the consumer, allowing for just-in-time transformations
    of proxy values.
    """

    def __init__(
        self,
        base: W,
        transformer: Callable[[Any], T] = lambda i: i,
    ) -> None:
        super().__init__()
        self.__proxy_root = base
        self.__transformer = transformer

    def __getitem__(self, key: Union[str, int]) -> T:
        value = self.__proxy_root[key]
        return self.__transformer(value)

    def __getattr__(self, key: str) -> T:
        try:
            value = self.__proxy_root[key]
        except KeyError:
            raise AttributeError(
                f"{type(self.__proxy_root).__name__} object has no attribute '{key}'"
            )
        # apply this outside of the access in case a KeyError occurs inside
        # of `__transformer`
        return self.__transformer(value)
