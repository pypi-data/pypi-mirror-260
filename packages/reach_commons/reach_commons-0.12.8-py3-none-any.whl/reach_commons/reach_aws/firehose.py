import base64
import json
import math
import os
from datetime import datetime
from functools import cached_property
from time import sleep

import boto3
from botocore.exceptions import ClientError

from reach_commons.app_logging.logger import get_reach_logger
from reach_commons.reach_aws.exceptions import KinesisClientException
from reach_commons.utils import remove_nulls


# noinspection PyMethodMayBeStatic
class BaseFirehoseClient:
    def __init__(
        self,
        logger=get_reach_logger(),
        region_name="us-east-1",
        profile_name=None,
    ):
        self.region_name = region_name
        self.profile_name = profile_name
        self.logger = logger

    def handle_exception(self, exc, secret, ciphertext):
        error_msg = (
            "error_kinesis_client, "
            "secret={}, "
            "ciphertext={!r}, "
            "error={!r}".format(secret, ciphertext, exc)
        )
        self.logger.error(error_msg)
        raise KinesisClientException(error_msg)


class FirehoseClient(BaseFirehoseClient):
    def __init__(self, delivery_stream_name=None):
        super().__init__()
        self.delivery_stream_name = (
            delivery_stream_name
            or f"{os.environ.get('ENV', 'Staging')}-kinesis-firehose-extended-s3-stream"
        )

    @cached_property
    def client(self):
        session = boto3.Session(
            region_name=self.region_name, profile_name=self.profile_name
        )
        return session.client("firehose")

    def notify_google_review_downloaded(
        self,
        business_id: int,
        method_name: str,
        object_payload,
        retry: int = 0,
    ):
        object_payload = (
            remove_nulls(object_payload)
            if isinstance(object_payload, dict)
            else object_payload
        )
        object_name = "GoogleReviewDownloaded"

        firehose_message = {
            "DateTime": str(datetime.now()),
            "MinuteGroup": int(15 * (math.floor(datetime.now().minute / 15))),
            "BusinessID": business_id,
            "ObjectName": object_name,
            "MethodName": method_name,
            "ObjectPayload": object_payload,
        }
        self.logger.info(
            "notify_firehose called for business_id={business_id}, object_name={object_name}, "
            "method_name={method_name}, object_payload={object_payload}, retry={retry}. "
            "Firehose message constructed: {firehose_message}".format(
                business_id=business_id,
                object_name=object_name,
                method_name=method_name,
                object_payload=json.dumps(object_payload)
                if isinstance(object_payload, dict)
                else object_payload,
                retry=retry,
                firehose_message=json.dumps(firehose_message),
            )
        )
        firehose_message = json.dumps(firehose_message)

        try:
            record = {"Data": firehose_message}
            response = self.client.put_record(
                DeliveryStreamName=self.delivery_stream_name,
                Record=record,
            )
            return response
        except Exception as ex:
            self.logger.exception(
                "An error occurred while trying to send data to Firehose", exc_info=ex
            )
            if retry < 20:
                sleep(1)
                return self.notify_google_review_downloaded(
                    business_id=business_id,
                    method_name=method_name,
                    object_payload=object_payload,
                    retry=retry + 1,
                )
