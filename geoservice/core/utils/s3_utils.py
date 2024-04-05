import logging

import boto3
from botocore.exceptions import ClientError
from core.constants import S3Constants
from django.conf import settings
from rest_framework.exceptions import ValidationError


class S3Utils:
    def __init__(self) -> None:
        self.s3_client = boto3.client(
            "s3",
            region_name=S3Constants.BUCKET_REGION,
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        )
        self.url_expiry = S3Constants.BUCKET_URL_EXPIRY
        self.aerial_view_bucket_name = S3Constants.AERIAL_VIEW_BUCKET_NAME

    def verify_s3_object(self, key):
        """Verify the S3 object.
        This function does a head check on the S3 object.

        Args:
            key(str): Key of the S3 object.
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            logging.error(e)
            raise ValidationError(
                {
                    "is_created": False,
                    "bucket_name": None,
                    "key": None,
                }
            )

        return {
            "is_created": True,
            "bucket_name": self.bucket_name,
            "key": key,
        }

    def put_object(self, body, bucket_name=None, key=None):
        """Put object in S3 bucket."""
        if key is None:
            raise ValidationError("Key cannot be None")

        if body is None:
            raise ValidationError("Body cannot be None")

        if bucket_name is None:
            raise ValidationError("Bucket name cannot be None")

        try:
            response = self.s3_client.put_object(Body=body, Bucket=bucket_name, Key=key)
        except ClientError as e:
            logging.error(e)
            raise ValidationError(f"Error uploading image {key} to S3: {str(e)}")

        return response
