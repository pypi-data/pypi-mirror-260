from typing import *
from os import environ


def env_with_fallback(*names: List[str]) -> Optional[str]:
    for name in names:
        if env_val := environ.get(name):
            return env_val
    return None
