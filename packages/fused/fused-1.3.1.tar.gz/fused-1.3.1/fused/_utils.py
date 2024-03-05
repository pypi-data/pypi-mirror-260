from typing import Any, Union

from fused.core._impl._udf_ops_impl import get_step_config_from_server

from .core._impl._reimports import AttrDict


class _PublicUtils:
    """
    A class designed to dynamically access utils of public UDFs, fetching their configuration
    from the server.

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


utils = _PublicUtils()
"""
A module to access public UDFs and their utilities.

Examples:

    This example shows how to access the `geo_buffer` function from the `common` UDF.
    ```py
    import fused
    import geopandas as gpd

    gdf = gpd.read_file('https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/11_DISTRICT_OF_COLUMBIA/11/tl_rd22_11_bg.zip')
    gdf_buffered = fused.public.common.geo_buffer(gdf, 10)
    ```

Public UDFs are listed at https://github.com/fusedio/udfs/tree/main/public
"""
