"""
Type annotations for kinesis-video-webrtc-storage service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesis_video_webrtc_storage/type_defs/)

Usage::

    ```python
    from types_aiobotocore_kinesis_video_webrtc_storage.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

import sys
from typing import Dict

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ResponseMetadataTypeDef",
    "JoinStorageSessionInputRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
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
JoinStorageSessionInputRequestTypeDef = TypedDict(
    "JoinStorageSessionInputRequestTypeDef",
    {
        "channelArn": str,
    },
)
EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
