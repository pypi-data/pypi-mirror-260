import json
import os
from decimal import Decimal
from functools import cached_property

import boto3
from botocore.exceptions import ClientError

from reach_commons.app_logging.logger import get_reach_logger
from reach_commons.reach_aws.exceptions import (
    SQSClientPublishError,
    SQSClientTopicNotFound,
)

MESSAGE_ATTRIBUTES_TYPE = {
    str: "String",
    int: "Number",
    Decimal: "Number",
    float: "Number",
    bytes: "Binary",
    list: "String.Array",
    tuple: "String.Array",
}

FALLBACK_MESSAGE_ATTRIBUTES_TYPE = "String"


# noinspection PyMethodMayBeStatic
class BaseSQSClient:
    def __init__(
        self,
        topic_name=None,
        logger=get_reach_logger(),
        region_name="us-east-1",
        profile_name=None,
    ):
        self.topic_name = topic_name
        self.logger = logger
        self.region_name = region_name
        self.profile_name = profile_name

    @staticmethod
    def _prepare_message_attributes(attributes):
        message_attributes = {}
        for key, value in attributes.items():
            attr_type = MESSAGE_ATTRIBUTES_TYPE.get(
                type(value), FALLBACK_MESSAGE_ATTRIBUTES_TYPE
            )
            value_key = "BinaryValue" if attr_type == "Binary" else "StringValue"
            if attr_type in ("String.Array", "Number"):
                value = json.dumps(value)
            elif attr_type == "String":
                value = str(value)
            message_attributes[key] = {
                "DataType": attr_type,
                value_key: value,
            }
        return message_attributes

    def handle_exception(self, exc, message_data, message_attributes):
        error_msg = (
            "error_publishing_message, "
            "topic_name={}, "
            "message_data={}, "
            "message_attributes={}, "
            "error={}".format(self.topic_name, message_data, message_attributes, exc)
        )
        self.logger.error(error_msg)
        if exc.response["Error"]["Code"] == "NotFound":
            raise SQSClientTopicNotFound(error_msg)
        raise SQSClientPublishError(error_msg)


class SQSClient(BaseSQSClient):
    @cached_property
    def client(self):
        session = boto3.Session(
            region_name=self.region_name, profile_name=self.profile_name
        )
        return session.client("sqs")

    def publish(self, message_data, delay_seconds=1, message_attributes=None):
        if delay_seconds is None or delay_seconds < 1:
            self.logger.warning("Invalid delay_seconds value. It must be at least 1.")
            return False

        if delay_seconds > 900:  # 15 minutes
            self.logger.warning(
                "Message delay exceeds 48 hours. Message not published."
            )
            return False
        message_attributes = message_attributes or {}
        message_attributes = self._prepare_message_attributes(message_attributes)

        self.logger.info(
            "topic_name={}, "
            "message_data={}, "
            "message_attributes={}".format(
                self.topic_name, message_data, message_attributes
            )
        )

        message = json.dumps(message_data)

        try:
            self.client.send_message(
                QueueUrl=self.topic_name,
                MessageBody=message,
                DelaySeconds=delay_seconds,
                MessageAttributes=message_attributes,
            )
        except ClientError as exc:
            self.handle_exception(exc, message_data, message_attributes)

        self.logger.info(
            "published_message, "
            "topic_name={}, "
            "message={}, "
            "message_attributes={}".format(self.topic_name, message, message_attributes)
        )

        return True


class MessageFilter:
    """
    A utility class responsible for filtering SQS messages based on the service name.

    Methods:
        filter_messages(service_name: str, event: dict) -> list:
            Filters messages from the provided event based on the service name.
    """

    @staticmethod
    def filter_messages(
        event,
        service_name=None,
        logger=get_reach_logger(),
    ):
        """
        Filter messages from the provided event based on the given service name.

        If the service_name is None or matches the service specified in the message attributes,
        the message is included in the returned list.

        Args:
        - service_name (str): The name of the service to filter messages for.
                             If None, all messages are returned.
        - event (dict): The event data containing SQS records.

        Returns:
        - list: A list of messages filtered based on the service name.
        """
        logger.info(event)
        messages = []

        for record in event.get("Records", []):
            message_body = (
                record["body"]
                if isinstance(record["body"], dict)
                else json.loads(record["body"])
            )

            if (
                not service_name
                or service_name
                == record["messageAttributes"]["service_name"]["stringValue"]
            ):
                messages.append(message_body)

        return messages


class HubspotSQSNotifier(SQSClient):
    """
    Example:
        hubspot_msg = HubspotSQSNotifier()
        hubspot_msg.notify_business_change(business_id=10293)
    """

    SERVICE_NAME = "HubspotSQSNotifier"
    TOPIC_NAME = "reach-data-bridge-messages-queue"
    DEFAULT_REGION = "us-east-1"

    def __init__(self, region_name=DEFAULT_REGION, logger=get_reach_logger()):
        super().__init__(
            region_name=region_name,
            logger=logger,
            topic_name=f"{os.environ.get('ENV', 'Staging')}-{self.TOPIC_NAME}",
        )

    def send_message(
        self, object_name, object_id, secondary_object_id=None, delay_seconds=1
    ):
        message_data = {
            "object_name": object_name,
            "object_id": object_id,
            "delay_seconds": delay_seconds,
        }
        if secondary_object_id is not None:
            message_data["secondary_object_id"] = secondary_object_id

        message_attributes = {"service_name": self.SERVICE_NAME}

        return self.publish(
            message_data=message_data,
            message_attributes=message_attributes,
            delay_seconds=delay_seconds,
        )

    def republish(self, message):
        delay_seconds = message.get("delay_seconds", 5)

        if "delay_seconds" in message:
            delay_seconds *= 2

        object_name = message["object_name"]
        object_id = message["object_id"]
        secondary_object_id = message.get("secondary_object_id")

        self.send_message(
            object_name=object_name,
            object_id=object_id,
            secondary_object_id=secondary_object_id,
            delay_seconds=delay_seconds,
        )

        return delay_seconds

    def notify_business_change(self, business_id, delay_seconds=1):
        return self.send_message(
            object_name="business_change",
            object_id=business_id,
            delay_seconds=delay_seconds,
        )

    def notify_user_change(self, user_id, delay_seconds=1):
        return self.send_message(
            object_name="user_change", object_id=user_id, delay_seconds=delay_seconds
        )

    def notify_user_business_change(self, user_id, business_id, delay_seconds=1):
        return self.send_message(
            object_name="user_business_change",
            object_id=user_id,
            secondary_object_id=business_id,
            delay_seconds=delay_seconds,
        )


class OutscraperSQSNotifier(SQSClient):
    SERVICE_NAME = "OutscraperSQSNotifier"
    TOPIC_NAME = "reach-data-bridge-messages-queue"
    DEFAULT_REGION = "us-east-1"

    def __init__(self, region_name=DEFAULT_REGION, logger=get_reach_logger()):
        super().__init__(
            region_name=region_name,
            logger=logger,
            topic_name=f"{os.environ.get('ENV', 'Staging')}-{self.TOPIC_NAME}",
        )

    def notify_for_google_reviews_sync(self, business_id, delay_seconds=1):
        message_data = {"business_id": business_id}

        message_attributes = {"service_name": self.SERVICE_NAME}

        return self.publish(
            message_data=message_data,
            message_attributes=message_attributes,
            delay_seconds=delay_seconds,
        )
