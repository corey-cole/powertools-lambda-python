from aws_lambda_powertools.utilities.data_classes import (
    CloudWatchCustomConnectorEvent,
    GetMetricDataResponse,
    MessageData,
    MetricDataResult,
)
from tests.functional.utils import load_event


def test_cloud_watch_custom_connector_get_metric_data_request_event():
    raw_event = load_event("cloudWatchGetMetricData.json")
    parsed_event = CloudWatchCustomConnectorEvent(raw_event)

    assert parsed_event.get_metric_data_request is not None

    request_context_raw = raw_event["GetMetricDataRequest"]
    assert parsed_event.get_metric_data_request.start_time == request_context_raw["StartTime"]
    assert parsed_event.get_metric_data_request.end_time == request_context_raw["EndTime"]
    assert parsed_event.get_metric_data_request.period == request_context_raw["Period"]
    assert parsed_event.get_metric_data_request.arguments == request_context_raw["Arguments"]


def test_cloud_watch_custom_connector_describe_event():
    parsed_event = CloudWatchCustomConnectorEvent({"EventType": "DescribeGetMetricData"})

    assert parsed_event.get_metric_data_request is None


def test_cloud_watch_custom_connector_get_metric_data_response_event():
    result_1 = MetricDataResult(
        label="CPUUtilization",
        timestamps=[1697060700, 1697061000, 1697061300],
        values=[ 15000, 14000, 16000 ],
    )
    response = GetMetricDataResponse(
        results=[result_1],
    )
    response_dict = response.asdict()
    print(response_dict)
    assert response_dict["MetricDataResults"][0]["Label"] == result_1.label
    assert response_dict["MetricDataResults"][0]["Timestamps"] == result_1.timestamps
    assert response_dict["MetricDataResults"][0]["Values"] == result_1.values
    assert response_dict["MetricDataResults"][0]["StatusCode"] == result_1.status_code
