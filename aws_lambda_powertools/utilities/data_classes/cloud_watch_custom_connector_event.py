import enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from typing_extensions import Literal

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


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
        return self["StartTime"]

    @property
    def end_time(self) -> int:
        return self["EndTime"]

    @property
    def period(self) -> int:
        return self["Period"]

    @property
    def arguments(self) -> List[Union[str, bool, int, float]]:
        return self["Arguments"]


class CloudWatchCustomConnectorEvent(DictWrapper):
    @property
    def event_type(self) -> CloudWatchCustomConnectorEventType:
        return self["EventType"]

    @property
    def get_metric_data_request(self) -> Optional[GetMetricDataRequest]:
        metric_data_request = self.get("GetMetricDataRequest")
        return None if metric_data_request is None else GetMetricDataRequest(metric_data_request)


@dataclass(repr=False, order=False)
class MessageData:
    code: Optional[str] = None
    value: Optional[str] = None

    def asdict(self) -> dict:
        response = {}
        if self.code is not None:
            response["Code"] = self.code
        if self.value is not None:
            response["Value"] = self.value
        return response


@dataclass(repr=False, order=False)
class MetricDataResult:
    status_code: Optional[Literal["Complete", "InternalError", "PartialData", "Forbidden"]] = "Complete"
    messages: Optional[List[MessageData]] = None
    label: Optional[str] = None
    timestamps: Optional[List[int]] = None
    values: Optional[List[Union[int, float]]] = None

    def asdict(self) -> dict:
        response = {
            "StatusCode": self.status_code,
        }
        for member in ["messages", "label", "timestamps", "values"]:
            if hasattr(self, member):
                print(f"Has attribute {member}")
                response[member.title()] = getattr(self, member)

        return response


@dataclass(repr=False, order=False)
class GetMetricDataResponse:
    error: Optional[MessageData] = None
    results: Optional[List[MetricDataResult]] = None

    def asdict(self) -> dict:
        response: Dict[str, Any] = {}
        if self.error is not None:
            response["Error"] = self.error.asdict()
        if self.results is not None:
            response["MetricDataResults"] = [result.asdict() for result in self.results]
        return response
