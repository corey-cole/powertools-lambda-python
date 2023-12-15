from aws_lambda_powertools.utilities.data_classes import (
    CloudWatchCustomConnectorEvent,
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
