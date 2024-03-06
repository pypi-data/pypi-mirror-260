from typing import *

if TYPE_CHECKING:
    from ..model.source import Source


def iterate_deep_source_traversal(source: "Source"):
    """
    Iterate over the provided source, first yielding the target, and continuing
    into it if it has dependent sources. The result is a depth first search
    _into_ the source. This can be useful for unwrapping a transformed
    source down to its original table or SQL components, for example.
    """
    from ..model.source_transform import TransformedSource

    stack = [source]
    while stack:
        curr = stack.pop()
        yield curr
        if isinstance(curr, TransformedSource):
            stack.append(curr.base)
