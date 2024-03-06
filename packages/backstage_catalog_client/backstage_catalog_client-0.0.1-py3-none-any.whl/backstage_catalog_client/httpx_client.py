from __future__ import annotations

from urllib.parse import urljoin

from httpx import AsyncClient

from backstage_catalog_client.catalog_api import (
    CATALOG_API_BASE_PATH,
    CatalogApi,
    get_filter_value,
)
from backstage_catalog_client.models import (
    CatalogRequestOptions,
    GetEntitiesRequest,
    GetEntitiesResponse,
)
from backstage_catalog_client.utils import to_dict


class HttpxClient(CatalogApi):
    def __init__(self, base_url: str, client: AsyncClient | None = None) -> None:
        self.catalog_api_path = urljoin(base_url, CATALOG_API_BASE_PATH)
        self.base_url = base_url
        if client is None:
            self.client = AsyncClient()
        else:
            self.client = client

    async def getEntities(
        self,
        request: GetEntitiesRequest | None = None,
        options: CatalogRequestOptions | None = None,
    ) -> GetEntitiesResponse:
        if request is None:
            request = GetEntitiesRequest()
        if options is None:
            options = CatalogRequestOptions()

        dict_request = to_dict(request)
        if request.entity_filter:
            del dict_request["entity_filter"]
            dict_request["filter"] = get_filter_value(request.entity_filter)

        response = await self.client.get(f"{self.catalog_api_path}/entities", params=dict_request)
        response.raise_for_status()

        return GetEntitiesResponse(items=response.json())
