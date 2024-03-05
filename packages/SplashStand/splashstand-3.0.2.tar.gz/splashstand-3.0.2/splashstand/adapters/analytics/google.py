import typing as t

from acb.depends import depends

from ._base import AnalyticsBase
from ._base import AnalyticsBaseSettings

# from google.analytics import admin_v1beta


class AnalyticsSettings(AnalyticsBaseSettings):
    measurement_id: str
    tracker: str
    view_id: str
    api_scope: t.Optional[str] = "https://www.googleapis.com/auth/analytics.readonly"
    days_line: list[int] = [30, 365]
    dimensions_table: list[str] = [
        "region",
        "city",
        "screenResolution",
        "browser",
        "operatingSystem",
    ]
    universal_tracker: t.Optional[str] = "UA-128993722-2"
    universal_measurement_id: t.Optional[str] = "G-1TXCMM7BVP"


class Analytics(AnalyticsBase):
    ...
    # client = admin_v1beta.AnalyticsAdminServiceAsyncClient()


depends.set(Analytics)
