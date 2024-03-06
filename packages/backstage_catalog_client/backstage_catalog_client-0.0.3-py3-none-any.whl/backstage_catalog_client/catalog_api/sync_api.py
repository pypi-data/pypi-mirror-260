from __future__ import annotations

from typing import Protocol

from backstage_catalog_client.models import (
    CatalogRequestOptions,
    GetEntitiesRequest,
    GetEntitiesResponse,
)


class SyncCatalogApi(Protocol):
    def get_entities(
        self,
        request: GetEntitiesRequest | None = None,
        options: CatalogRequestOptions | None = None,
    ) -> GetEntitiesResponse:
        """
        Gets entities from your backstage instance.

        Args:
            request: The request object for getting entities. Defaults to None.
            options: The options for the catalog request. Defaults to None.

        Returns:
            The response object containing the entities.
        """
        ...
