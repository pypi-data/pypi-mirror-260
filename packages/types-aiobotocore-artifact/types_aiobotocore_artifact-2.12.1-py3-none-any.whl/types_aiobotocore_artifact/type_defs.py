"""
Type annotations for artifact service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/type_defs/)

Usage::

    ```python
    from types_aiobotocore_artifact.type_defs import AccountSettingsTypeDef

    data: AccountSettingsTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List

from .literals import (
    AcceptanceTypeType,
    NotificationSubscriptionStatusType,
    PublishedStateType,
    UploadStateType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AccountSettingsTypeDef",
    "ResponseMetadataTypeDef",
    "GetReportMetadataRequestRequestTypeDef",
    "ReportDetailTypeDef",
    "GetReportRequestRequestTypeDef",
    "GetTermForReportRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListReportsRequestRequestTypeDef",
    "ReportSummaryTypeDef",
    "PutAccountSettingsRequestRequestTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "GetReportResponseTypeDef",
    "GetTermForReportResponseTypeDef",
    "PutAccountSettingsResponseTypeDef",
    "GetReportMetadataResponseTypeDef",
    "ListReportsRequestListReportsPaginateTypeDef",
    "ListReportsResponseTypeDef",
)

AccountSettingsTypeDef = TypedDict(
    "AccountSettingsTypeDef",
    {
        "notificationSubscriptionStatus": NotRequired[NotificationSubscriptionStatusType],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
GetReportMetadataRequestRequestTypeDef = TypedDict(
    "GetReportMetadataRequestRequestTypeDef",
    {
        "reportId": str,
        "reportVersion": NotRequired[int],
    },
)
ReportDetailTypeDef = TypedDict(
    "ReportDetailTypeDef",
    {
        "acceptanceType": NotRequired[AcceptanceTypeType],
        "arn": NotRequired[str],
        "category": NotRequired[str],
        "companyName": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "deletedAt": NotRequired[datetime],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "lastModifiedAt": NotRequired[datetime],
        "name": NotRequired[str],
        "periodEnd": NotRequired[datetime],
        "periodStart": NotRequired[datetime],
        "productName": NotRequired[str],
        "sequenceNumber": NotRequired[int],
        "series": NotRequired[str],
        "state": NotRequired[PublishedStateType],
        "statusMessage": NotRequired[str],
        "termArn": NotRequired[str],
        "uploadState": NotRequired[UploadStateType],
        "version": NotRequired[int],
    },
)
GetReportRequestRequestTypeDef = TypedDict(
    "GetReportRequestRequestTypeDef",
    {
        "reportId": str,
        "termToken": str,
        "reportVersion": NotRequired[int],
    },
)
GetTermForReportRequestRequestTypeDef = TypedDict(
    "GetTermForReportRequestRequestTypeDef",
    {
        "reportId": str,
        "reportVersion": NotRequired[int],
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ListReportsRequestRequestTypeDef = TypedDict(
    "ListReportsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
ReportSummaryTypeDef = TypedDict(
    "ReportSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "category": NotRequired[str],
        "companyName": NotRequired[str],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "periodEnd": NotRequired[datetime],
        "periodStart": NotRequired[datetime],
        "productName": NotRequired[str],
        "series": NotRequired[str],
        "state": NotRequired[PublishedStateType],
        "statusMessage": NotRequired[str],
        "uploadState": NotRequired[UploadStateType],
        "version": NotRequired[int],
    },
)
PutAccountSettingsRequestRequestTypeDef = TypedDict(
    "PutAccountSettingsRequestRequestTypeDef",
    {
        "notificationSubscriptionStatus": NotRequired[NotificationSubscriptionStatusType],
    },
)
GetAccountSettingsResponseTypeDef = TypedDict(
    "GetAccountSettingsResponseTypeDef",
    {
        "accountSettings": AccountSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetReportResponseTypeDef = TypedDict(
    "GetReportResponseTypeDef",
    {
        "documentPresignedUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetTermForReportResponseTypeDef = TypedDict(
    "GetTermForReportResponseTypeDef",
    {
        "documentPresignedUrl": str,
        "termToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
PutAccountSettingsResponseTypeDef = TypedDict(
    "PutAccountSettingsResponseTypeDef",
    {
        "accountSettings": AccountSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetReportMetadataResponseTypeDef = TypedDict(
    "GetReportMetadataResponseTypeDef",
    {
        "reportDetails": ReportDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListReportsRequestListReportsPaginateTypeDef = TypedDict(
    "ListReportsRequestListReportsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListReportsResponseTypeDef = TypedDict(
    "ListReportsResponseTypeDef",
    {
        "nextToken": str,
        "reports": List[ReportSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
