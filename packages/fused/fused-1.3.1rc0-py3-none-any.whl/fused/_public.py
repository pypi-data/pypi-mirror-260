from typing import Any, Union

from fused.core._impl._udf_ops_impl import get_step_config_from_server

from .core._impl._reimports import AttrDict


class _Public:
    """
    A class designed to dynamically access attributes or items, fetching their configuration
    from a server if they are not directly accessible as class attributes.

    Methods:
        __init__(self, cache_key: Any = None): Initializes the _Public instance with an optional cache key.
        __getattribute__(self, key: str) -> Union[Any, AttrDict]: Attempts to access class attributes, falling back to fetching the attribute's configuration from a server if not found.
        __getitem__(self, key: str) -> AttrDict: Fetches the configuration for the given key from a server and returns a utility object for execution.
    """

    def __init__(self, cache_key: Any = None):
        """
        Initializes the _Public instance with an optional cache key.

        Parameters:
            cache_key (Any, optional): A key used for caching purposes. Defaults to None.
        """
        self._cache_key = cache_key

    def __getattribute__(self, key: str) -> Union[Any, AttrDict]:
        try:
            return super().__getattribute__(key)
        except AttributeError:
            try:
                return self[key]
            # Note that we need to raise an AttributeError, **not a KeyError** so that
            # IPython's _repr_html_ works here
            except KeyError:
                raise AttributeError(
                    f"object of type {type(self).__name__} has no attribute {key}"
                ) from None

    def __getitem__(self, key: str) -> AttrDict:
        step_config = get_step_config_from_server(
            email=None,
            slug=key,
            cache_key=self._cache_key,
            _is_public=True,
        )

        return step_config.udf.utils


public = _Public()
"""
A class designed to dynamically access attributes or items, fetching their configuration
from a server if they are not directly accessible as class attributes.
"""
