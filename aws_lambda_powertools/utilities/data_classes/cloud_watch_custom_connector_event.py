import enum
from typing import List, Optional, Union

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class MessageData(DictWrapper):
    @property
    def code(self) -> str:
        return self.get("Code")

    @property
    def value(self) -> str:
        return self.get("Value")


class StatusCode(enum.Enum):
    COMPLETE = "Complete"
    INTERNAL_ERROR = "InternalError"
    PARTIAL_DATA = "PartialData"
    FORBIDDEN = "Forbidden"


class CloudWatchCustomConnectorEventType(enum.Enum):
    GET_METRIC_DATA = "GetMetricData"
    DESCRIBE_GET_METRIC_DATA = "DescribeGetMetricData"


class GetMetricDataRequest(DictWrapper):
    @property
    def start_time(self) -> int:
        return self.get("StartTime")

    @property
    def end_time(self) -> int:
        return self.get("EndTime")

    @property
    def period(self) -> int:
        return self.get("Period")

    @property
    def arguments(self) -> List[Union[str, bool, int, float]]:
        return self.get("Arguments")


class CloudWatchCustomConnectorEvent(DictWrapper):
    @property
    def event_type(self) -> CloudWatchCustomConnectorEventType:
        return self.get("EventType")

    @property
    def get_metric_data_request(self) -> Optional[GetMetricDataRequest]:
        metric_data_request = self.get("GetMetricDataRequest")
        return None if metric_data_request is None else GetMetricDataRequest(metric_data_request)
