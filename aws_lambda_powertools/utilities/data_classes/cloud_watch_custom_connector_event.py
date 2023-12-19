import enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from typing_extensions import Literal

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class CloudWatchCustomConnectorEventType(enum.Enum):
    GET_METRIC_DATA = "GetMetricData"
    DESCRIBE_GET_METRIC_DATA = "DescribeGetMetricData"


class GetMetricDataRequest(DictWrapper):
    @property
    def start_time(self) -> int:
        """The timestamp specifying the earliest data to return. The Type is timestamp epoch seconds."""
        return self["StartTime"]

    @property
    def end_time(self) -> int:
        """The timestamp specifying the latest data to return. The Type is timestamp epoch seconds."""
        return self["EndTime"]

    @property
    def period(self) -> int:
        """The number of seconds that each aggregation of the metrics data represents. The minimum is 60 seconds."""
        return self["Period"]

    @property
    def arguments(self) -> List[Union[str, bool, int, float]]:
        """An array of arguments to pass to the Lambda metric math expression."""
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
    """A message returned by the GetMetricDataAPI, including a code and a description.

    Parameters
    ----------
    code: Optional[str]
        The error code or status code associated with the message.
    value: Optional[str]
        The message text.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MessageData.html
    """

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
    """A GetMetricData call returns an array of MetricDataResult structures.
       Each of these structures includes the data points for that metric, along with the timestamps of those data points
       and other identifying information.

    Parameters
    ----------
    status_code: Optional[Literal["Complete", "InternalError", "PartialData", "Forbidden"]]
        The status of the returned data.
    messages: Optional[List[MessageData]]
        A list of messages with additional information about the data returned.
    label: Optional[str]
        The human-readable label associated with the data.
    timestamps: Optional[List[int]]
        The timestamps for the data points, formatted in Unix timestamp format.
    values: Optional[List[Union[int, float]]]
        The data points for the metric corresponding to Timestamps.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_MultiDataSources-Connect-Custom.html#MultiDataSources-GetMetricData
    - https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDataResult.html

    """

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
                response[member.title()] = getattr(self, member)
        return response


@dataclass(repr=False, order=False)
class GetMetricDataResponse:
    """GetMetricData response object.

    Parameters:
    -----------
    error: Optional[MessageData]
        Error response to caller.  MessageData `Value` will be displayed in the CloudWatch console.
    results: List[MetricDataResult]
        List of time-series data.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_MultiDataSources-Connect-Custom.html#MultiDataSources-GetMetricData
    """

    error: Optional[MessageData] = None
    results: List[MetricDataResult] = []

    def asdict(self) -> dict:
        response: Dict[str, Any] = {}
        if self.error is not None:
            # If 'Error' is present, only return that.  Otherwise CloudWatch gets upset
            return {
                "Error": self.error.asdict(),
            }
        # Failing to return a result with this key results in a warning in the CloudWatch console
        response["MetricDataResults"] = [result.asdict() for result in self.results or []]
        return response
