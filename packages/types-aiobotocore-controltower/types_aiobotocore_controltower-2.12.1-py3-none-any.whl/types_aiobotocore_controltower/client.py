"""
Type annotations for controltower service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_controltower.client import ControlTowerClient

    session = get_session()
    async with session.create_client("controltower") as client:
        client: ControlTowerClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListBaselinesPaginator,
    ListEnabledBaselinesPaginator,
    ListEnabledControlsPaginator,
    ListLandingZonesPaginator,
)
from .type_defs import (
    CreateLandingZoneOutputTypeDef,
    DeleteLandingZoneOutputTypeDef,
    DisableBaselineOutputTypeDef,
    DisableControlOutputTypeDef,
    EnableBaselineOutputTypeDef,
    EnableControlOutputTypeDef,
    EnabledBaselineFilterTypeDef,
    EnabledBaselineParameterTypeDef,
    EnabledControlParameterTypeDef,
    GetBaselineOperationOutputTypeDef,
    GetBaselineOutputTypeDef,
    GetControlOperationOutputTypeDef,
    GetEnabledBaselineOutputTypeDef,
    GetEnabledControlOutputTypeDef,
    GetLandingZoneOperationOutputTypeDef,
    GetLandingZoneOutputTypeDef,
    ListBaselinesOutputTypeDef,
    ListEnabledBaselinesOutputTypeDef,
    ListEnabledControlsOutputTypeDef,
    ListLandingZonesOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ResetEnabledBaselineOutputTypeDef,
    ResetLandingZoneOutputTypeDef,
    UpdateEnabledBaselineOutputTypeDef,
    UpdateEnabledControlOutputTypeDef,
    UpdateLandingZoneOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ControlTowerClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ControlTowerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ControlTowerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#close)
        """

    async def create_landing_zone(
        self, *, manifest: Mapping[str, Any], version: str, tags: Mapping[str, str] = ...
    ) -> CreateLandingZoneOutputTypeDef:
        """
        Creates a new landing zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.create_landing_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#create_landing_zone)
        """

    async def delete_landing_zone(
        self, *, landingZoneIdentifier: str
    ) -> DeleteLandingZoneOutputTypeDef:
        """
        Decommissions a landing zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.delete_landing_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#delete_landing_zone)
        """

    async def disable_baseline(
        self, *, enabledBaselineIdentifier: str
    ) -> DisableBaselineOutputTypeDef:
        """
        Disable an `EnabledBaseline` resource on the specified Target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.disable_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#disable_baseline)
        """

    async def disable_control(
        self, *, controlIdentifier: str, targetIdentifier: str
    ) -> DisableControlOutputTypeDef:
        """
        This API call turns off a control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.disable_control)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#disable_control)
        """

    async def enable_baseline(
        self,
        *,
        baselineIdentifier: str,
        baselineVersion: str,
        targetIdentifier: str,
        parameters: Sequence[EnabledBaselineParameterTypeDef] = ...,
        tags: Mapping[str, str] = ...,
    ) -> EnableBaselineOutputTypeDef:
        """
        Enable (apply) a `Baseline` to a Target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.enable_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#enable_baseline)
        """

    async def enable_control(
        self,
        *,
        controlIdentifier: str,
        targetIdentifier: str,
        parameters: Sequence[EnabledControlParameterTypeDef] = ...,
        tags: Mapping[str, str] = ...,
    ) -> EnableControlOutputTypeDef:
        """
        This API call activates a control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.enable_control)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#enable_control)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#generate_presigned_url)
        """

    async def get_baseline(self, *, baselineIdentifier: str) -> GetBaselineOutputTypeDef:
        """
        Retrieve details about an existing `Baseline` resource by specifying its
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_baseline)
        """

    async def get_baseline_operation(
        self, *, operationIdentifier: str
    ) -> GetBaselineOperationOutputTypeDef:
        """
        Returns the details of an asynchronous baseline operation, as initiated by any
        of these APIs: `EnableBaseline`, `DisableBaseline`, `UpdateEnabledBaseline`,
        `ResetEnabledBaseline`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_baseline_operation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_baseline_operation)
        """

    async def get_control_operation(
        self, *, operationIdentifier: str
    ) -> GetControlOperationOutputTypeDef:
        """
        Returns the status of a particular `EnableControl` or `DisableControl`
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_control_operation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_control_operation)
        """

    async def get_enabled_baseline(
        self, *, enabledBaselineIdentifier: str
    ) -> GetEnabledBaselineOutputTypeDef:
        """
        Retrieve details of an `EnabledBaseline` resource by specifying its identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_enabled_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_enabled_baseline)
        """

    async def get_enabled_control(
        self, *, enabledControlIdentifier: str
    ) -> GetEnabledControlOutputTypeDef:
        """
        Retrieves details about an enabled control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_enabled_control)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_enabled_control)
        """

    async def get_landing_zone(self, *, landingZoneIdentifier: str) -> GetLandingZoneOutputTypeDef:
        """
        Returns details about the landing zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_landing_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_landing_zone)
        """

    async def get_landing_zone_operation(
        self, *, operationIdentifier: str
    ) -> GetLandingZoneOperationOutputTypeDef:
        """
        Returns the status of the specified landing zone operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_landing_zone_operation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_landing_zone_operation)
        """

    async def list_baselines(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListBaselinesOutputTypeDef:
        """
        Returns a summary list of all available baselines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.list_baselines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#list_baselines)
        """

    async def list_enabled_baselines(
        self,
        *,
        filter: EnabledBaselineFilterTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListEnabledBaselinesOutputTypeDef:
        """
        Returns a list of summaries describing `EnabledBaseline` resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.list_enabled_baselines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#list_enabled_baselines)
        """

    async def list_enabled_controls(
        self, *, targetIdentifier: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListEnabledControlsOutputTypeDef:
        """
        Lists the controls enabled by Amazon Web Services Control Tower on the
        specified organizational unit and the accounts it
        contains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.list_enabled_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#list_enabled_controls)
        """

    async def list_landing_zones(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListLandingZonesOutputTypeDef:
        """
        Returns the landing zone ARN for the landing zone deployed in your managed
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.list_landing_zones)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#list_landing_zones)
        """

    async def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        Returns a list of tags associated with the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#list_tags_for_resource)
        """

    async def reset_enabled_baseline(
        self, *, enabledBaselineIdentifier: str
    ) -> ResetEnabledBaselineOutputTypeDef:
        """
        Re-enables an `EnabledBaseline` resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.reset_enabled_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#reset_enabled_baseline)
        """

    async def reset_landing_zone(
        self, *, landingZoneIdentifier: str
    ) -> ResetLandingZoneOutputTypeDef:
        """
        This API call resets a landing zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.reset_landing_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#reset_landing_zone)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Applies tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#untag_resource)
        """

    async def update_enabled_baseline(
        self,
        *,
        baselineVersion: str,
        enabledBaselineIdentifier: str,
        parameters: Sequence[EnabledBaselineParameterTypeDef] = ...,
    ) -> UpdateEnabledBaselineOutputTypeDef:
        """
        Updates an `EnabledBaseline` resource's applied parameters or version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.update_enabled_baseline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#update_enabled_baseline)
        """

    async def update_enabled_control(
        self, *, enabledControlIdentifier: str, parameters: Sequence[EnabledControlParameterTypeDef]
    ) -> UpdateEnabledControlOutputTypeDef:
        """
        Updates the configuration of an already enabled control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.update_enabled_control)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#update_enabled_control)
        """

    async def update_landing_zone(
        self, *, landingZoneIdentifier: str, manifest: Mapping[str, Any], version: str
    ) -> UpdateLandingZoneOutputTypeDef:
        """
        This API call updates the landing zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.update_landing_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#update_landing_zone)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_baselines"]) -> ListBaselinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_enabled_baselines"]
    ) -> ListEnabledBaselinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_enabled_controls"]
    ) -> ListEnabledControlsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_landing_zones"]
    ) -> ListLandingZonesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/#get_paginator)
        """

    async def __aenter__(self) -> "ControlTowerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/controltower.html#ControlTower.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/client/)
        """
