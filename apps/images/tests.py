import boto3
import requests

from moto import mock_s3

from django.conf import settings
from rest_framework import status

from rest_framework.test import APITestCase, APIClient

from apps.contrib import storage
from apps.contrib.storage import (
    generate_presigned_post,
    check_file_exists,
    generate_presigned_url,
)

# Override AWS setting (Please don't change this, this might delete s3 data)
settings.AWS_ACCESS_KEY_ID = "testing"
settings.AWS_SECRET_ACCESS_KEY = "testing"
settings.AWS_SECURITY_TOKEN = "testing"
settings.AWS_SESSION_TOKEN = "testing"
settings.AWS_BUCKET_REGION = "us-east-1"
settings.AWS_BUCKET_NAME = "bucket"
settings.AWS_S3_ENDPOINT_URL = "http://127.0.0.1:5000"


class ImageTestCase(APITestCase):
    # Init moto
    mock_s3 = mock_s3()

    def setUp(self):
        self.mock_s3.start()

        # Init Client
        self.client = APIClient()

        # Init boto3 s3 client
        self.s3 = boto3.client(
            "s3", endpoint_url="http://127.0.0.1:5000", region_name="us-east-1"
        )

        # Override storage s3
        storage.s3 = self.s3

        self.s3.create_bucket(Bucket=settings.AWS_BUCKET_NAME)

    def tearDown(self):
        # Delete all objects in s3 bucket
        objects = self.s3.list_objects(Bucket=settings.AWS_BUCKET_NAME).get("Contents")
        if objects:
            for obj in objects:
                self.s3.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=obj["Key"])

        # Bucket can only delete, if all objects are deleted
        self.s3.delete_bucket(Bucket=settings.AWS_BUCKET_NAME)

        self.mock_s3.stop()

    def test_presigned_post_url(self):
        """
        Test presigned_post_url method
        """
        key = "test/car.jpg"
        response = generate_presigned_post(key)
        fields = response.get("fields")

        # Checking key before upload
        self.assertEqual(check_file_exists(key), False)

        # POST method over response data
        url = response.get("url")
        payload = fields
        files = [
            (
                "file",
                (
                    "original.jpg",
                    open("data/images/car.jpg", "rb"),
                    "image/jpeg",
                ),
            )
        ]
        requests.request("POST", url, data=payload, files=files)

        # Checking key before upload
        self.assertEqual(check_file_exists(key), True)

    def test_presigned_url(self):
        """
        Test presigned_url method that will give signed file url
        """
        key = "test/flower.png"
        response = generate_presigned_post(key)
        fields = response.get("fields")

        # Checking key and url before upload
        self.assertEqual(check_file_exists(key), False)
        file_url = generate_presigned_url(key)
        res = requests.request("GET", file_url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # POST method over response data
        url = response.get("url")
        payload = fields
        files = [
            (
                "file",
                (
                    "flower.png",
                    open("data/images/flower.png", "rb"),
                    "image/png",
                ),
            )
        ]
        requests.request("POST", url, data=payload, files=files)

        # Checking key and url after upload
        self.assertEqual(check_file_exists(key), True)
        file_url = generate_presigned_url(key)
        res = requests.request("GET", file_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_image_upload_with_wrong_format(self):
        """
        Test image upload with wrong format. Only accepts (.png, .jpg, .jpeg)
        """
        file_name = "sample.gif"
        request = self.client.post(
            "/api/images/upload", {"name": file_name, "mimetype": "image/png"}
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

        file_name = "sample.svg"
        request = self.client.post(
            "/api/images/upload", {"name": file_name, "mimetype": "image/png"}
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_upload_with_wrong_format(self):
        """
        Test image upload with wrong mimetype. Only accepts (image/png, image/jpg, image/jpeg)
        """
        file_name = "sample.jpeg"
        request = self.client.post(
            "/api/images/upload", {"name": file_name, "mimetype": "image/gif"}
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

        file_name = "sample.png"
        request = self.client.post(
            "/api/images/upload", {"name": file_name, "mimetype": "image/jpeg"}
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_upload_endpoint(self):
        """
        Test image upload endpoint
        """
        file_name = "sample.jpg"
        request = self.client.post(
            "/api/images/upload", {"name": file_name, "mimetype": "image/jpg"}
        )
        response = request.json()
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        image_id = response.get("id")
        fields = response.get("presigned_post_url").get("fields")
        url = response.get("presigned_post_url").get("url")
        key = fields.get("key")

        # Checking key and url before upload
        self.assertEqual(check_file_exists(key), False)
        file_url = generate_presigned_url(key)
        res = requests.request("GET", file_url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # POST method over response data
        url = url
        payload = fields
        files = [
            (
                "file",
                (
                    key,
                    open("data/images/car.jpg", "rb"),
                    "image/jpg",
                ),
            )
        ]

        response = requests.request("POST", url, data=payload, files=files)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Checking key and url after upload
        self.assertEqual(check_file_exists(key), True)
        file_url = generate_presigned_url(key)
        res = requests.request("GET", file_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_image_get_endpoint(self):
        """
        Test image get endpoint
        """
        file_name = "sample.png"
        request = self.client.post(
            "/api/images/upload", {"name": file_name, "mimetype": "image/png"}
        )
        response = request.json()
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        image_id = response.get("id")
        fields = response.get("presigned_post_url").get("fields")
        url = response.get("presigned_post_url").get("url")
        key = fields.get("key")

        # Checking key and url before upload
        self.assertEqual(check_file_exists(key), False)

        # Get endpoint calling before upload
        request = self.client.get(f"/api/images/{image_id}/")
        response = request.json()
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Checking response image url
        res = requests.request("GET", response.get("presigned_url"))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # POST method over response data
        url = url
        payload = fields
        files = [
            (
                "file",
                (
                    key,
                    open("data/images/flower.png", "rb"),
                    "image/png",
                ),
            )
        ]

        response = requests.request("POST", url, data=payload, files=files)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Checking key and url after upload
        self.assertEqual(check_file_exists(key), True)

        # Get endpoint calling after upload
        request = self.client.get(f"/api/images/{image_id}/")
        response = request.json()
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Checking response image url
        res = requests.request("GET", response.get("presigned_url"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
