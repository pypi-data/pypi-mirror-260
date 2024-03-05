from functools import wraps
from typing import Callable, Optional

from anyscale.service._private.sdk import ServiceSDK
from anyscale.service.models import ServiceConfig, ServiceStatus


_LAZY_GLOBAL_SDK: Optional[ServiceSDK] = None


def _inject_global_sdk(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global _LAZY_GLOBAL_SDK

        if _LAZY_GLOBAL_SDK is None:
            _LAZY_GLOBAL_SDK = ServiceSDK()

        return f(*args, _sdk=_LAZY_GLOBAL_SDK, **kwargs)

    return wrapper


@_inject_global_sdk
def deploy(
    config: ServiceConfig,
    *,
    in_place: bool = False,
    canary_percent: Optional[int] = None,
    max_surge_percent: Optional[int] = None,
    _sdk: ServiceSDK,
):
    return _sdk.deploy(
        config,
        in_place=in_place,
        canary_percent=canary_percent,
        max_surge_percent=max_surge_percent,
    )


@_inject_global_sdk
def status(name: Optional[str], *, _sdk: ServiceSDK) -> ServiceStatus:
    return _sdk.status(name=name)
