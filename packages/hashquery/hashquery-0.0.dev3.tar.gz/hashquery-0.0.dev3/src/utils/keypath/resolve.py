from typing import *
import inspect
from functools import wraps

from .keypath import (
    KeyPath,
    KeyPathComponentProperty,
    KeyPathComponentSubscript,
    KeyPathComponentCall,
    BoundKeyPath,
)


def get_keypath_resolver(keypath: KeyPath) -> Callable[[Any], Any]:
    """
    Given a keypath, returns it as a callable accessor function.
    """

    def resolver(root: Any) -> Any:
        current = root
        if type(keypath) == BoundKeyPath:
            current = keypath._bound_root

        for component in keypath._key_path_components:
            if type(component) is KeyPathComponentProperty:
                current = getattr(current, component.name)
            elif type(component) is KeyPathComponentSubscript:
                current = current[component.key]
            elif type(component) is KeyPathComponentCall:
                current = current(
                    *resolve_all_nested_keypaths(root, component.args),
                    **resolve_all_nested_keypaths(root, component.kwargs),
                )
            else:
                raise AssertionError(f"Invalid keypath component: {type(component)}")
        return current

    return resolver


def resolve_keypath(root: Any, keypath: KeyPath) -> Any:
    """
    Given a root and a KeyPath, resolves the keypath for that root
    and returns the final result (or fails with `AttributeError` if the
    keypath is invalid for that root).
    """
    return get_keypath_resolver(keypath)(root)


def resolve_all_nested_keypaths(root: Any, values) -> Any:
    """
    Given a data structure that may have KeyPaths in it, resolves all of them
    recursively with the provided root. This is helpful for handling collections
    of values that may or may not be KeyPaths, and turning them all into real
    values.
    """
    if type(values) is dict:
        return {
            key: resolve_all_nested_keypaths(root, nested)
            for key, nested in values.items()
        }
    elif type(values) is list:
        return [resolve_all_nested_keypaths(root, nested) for nested in values]
    elif type(values) is tuple:
        return (resolve_all_nested_keypaths(root, nested) for nested in values)
    elif isinstance(values, KeyPath):
        return resolve_keypath(root, values)
    else:
        return values


def resolve_keypath_args_from(root_keypath: KeyPath):
    """
    Decorates a function to convert its arguments to KeyPaths, using
    one of the arguments as the root for the others.

    The passed KeyPath is used to point to the root. It must start
    with a property access against a value matching one of the parameters'
    by name.

    For example, you can easily allow accessing `self` properties within a
    method. Let's assume I have a method of the form::

        def set_primary_date(self, date_column):

    and I want to allow consumers to write::

        model.set_primary_date(_.timestamp)

    instead of::

        model.set_primary_date(model.attributes.timestamp)

    I can do so by applying the decorator::

        @resolve_keypath_args_from(_.self.attributes)
        def set_primary_date(self, date_column):
    """

    def wrap(func):
        root_keypath_first_access = root_keypath._key_path_components[0]
        if not type(root_keypath_first_access) is KeyPathComponentProperty:
            raise AssertionError(
                "KeyPath for args decorator root must begin with property access"
            )
        root_keypath_after_first_prop = KeyPath(root_keypath._key_path_components[1:])

        # determine the index the root_keypath is pointing to, for
        # mapping `args` to the keypath value
        root_keypath_arg_idx = next(
            (
                i
                for i, param in enumerate(
                    list(inspect.signature(func).parameters.values())
                )
                if param.kind != inspect.Parameter.KEYWORD_ONLY
                and param.name == root_keypath_first_access.name
            ),
            None,
        )

        @wraps(func)
        def resolved_arg_func(*args, **kwargs):
            # The user can pass in the target root either inside of `*args`
            # or inside of `**kwargs`. We need to determine where it is.
            # and then resolve it from there

            if root_keypath_first_access.name in kwargs:
                root = resolve_keypath(
                    kwargs[root_keypath_first_access.name],
                    root_keypath_after_first_prop,
                )
            else:
                root = resolve_keypath(
                    args[root_keypath_arg_idx],
                    root_keypath_after_first_prop,
                )

            # apply the underlying function
            return func(
                *resolve_all_nested_keypaths(root, args),
                **resolve_all_nested_keypaths(root, kwargs),
            )

        return resolved_arg_func

    return wrap
