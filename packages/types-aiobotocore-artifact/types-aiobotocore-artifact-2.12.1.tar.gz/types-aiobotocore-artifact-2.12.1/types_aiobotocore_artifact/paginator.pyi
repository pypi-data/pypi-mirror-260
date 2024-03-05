"""
Type annotations for artifact service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_artifact.client import ArtifactClient
    from types_aiobotocore_artifact.paginator import (
        ListReportsPaginator,
    )

    session = get_session()
    with session.create_client("artifact") as client:
        client: ArtifactClient

        list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    ```
"""

from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListReportsResponseTypeDef, PaginatorConfigTypeDef

__all__ = ("ListReportsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListReportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Paginator.ListReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listreportspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Paginator.ListReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/paginators/#listreportspaginator)
        """
