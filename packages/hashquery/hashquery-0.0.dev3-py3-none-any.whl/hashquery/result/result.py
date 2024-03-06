from typing import *


class Result(Protocol):
    # defined with a magic method syntax since consumers shouldn't actually
    # call this; it's meant for the internal use of the runtime.
    def __result__(self):
        """
        Must return a value that a HashQuery client knows how to render.
        This return value must be pre-serialized.
        """
        ...
