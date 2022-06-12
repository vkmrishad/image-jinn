from celery.utils.log import get_task_logger
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from apps.contrib.storage import (
    check_file_exists,
    generate_presigned_url,
    download_fileobj,
    upload_fileobj,
)
from apps.images.choices import UploadStatus
from apps.images.models import Image
from apps.images.tasks import process_image_upload
from apps.images.serializers import (
    ImageSerializer,
    ImageUploadFinishedInputSerializer,
    ImageUploadSerializer,
    ImageRetrieveQuerySerializer,
)

logger = get_task_logger(__name__)


class ImageUploadViewSet(CreateModelMixin, GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        """
        This endpoint will help to create a s3 presigned post url.
        Using presigned post url, it's easy to upload image and will be synced with DB
        """
        instance = super().create(request, *args, **kwargs)

        try:
            # Update available extensions
            image = Image.objects.get(id=instance.data.get("id"))
            extension = image.name.split(".")[-1]
            image.available_extensions.append(extension)
            image.save()
        except Exception as e:
            logger.error("Image Conversion Error", e)
            raise ValidationError(
                {"error": "Something went wrong, while doing image conversion"}
            )

        # task will execute after 5 minutes to verify file uploaded
        process_image_upload.s(image.id).apply_async(countdown=300)
        return Response(
            self.get_serializer(image, many=False).data, status=status.HTTP_201_CREATED
        )


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "patch", "partial_update"]

    @extend_schema(parameters=[ImageRetrieveQuerySerializer])
    def retrieve(self, request, *args, **kwargs):
        """
        This endpoint will give image details.

        :param extension: Different image formats can be returned by using a different image file type
        """
        query_serializer = ImageRetrieveQuerySerializer(data=self.request.query_params)
        query_serializer.is_valid(raise_exception=True)
        query_params = query_serializer.data

        instance = self.get_object()
        extension = query_params.get("extension")

        if extension:
            serializer = self.get_serializer(instance)

            key = instance.key
            old_extension = key.split(".")[-1]

            # Extensions dict for easy mimtype mapping
            extensions = {
                "jpg": "image/jpg",
                "jpeg": "image/jpeg",
                "png": "image/png",
            }

            try:
                # Only do image conversion, if image extension is not same
                if old_extension != extension:
                    new_key = f"images/{instance.id}/image-{instance.id}.{extension}"

                    # If converted file not exits, download image to memory and upload with converted file back to s3
                    if not check_file_exists(new_key):
                        fileobj = download_fileobj(key)
                        upload_fileobj(
                            new_key, fileobj
                        )  # Todo: Need to convert with actual encoding

                        # Update available extensions
                        instance.available_extensions.append(extension)
                        instance.save()

                    # Update data with new values
                    data = serializer.data
                    data[
                        "name"
                    ] = f"{''.join(instance.name.split('.')[:-1])}.{extension}"
                    data["mimetype"] = extensions.get(extension.lower())
                    data["presigned_url"] = generate_presigned_url(new_key)
                    return Response(data)
            except Exception as e:
                logger.error("Image Conversion Error", e)
                raise ValidationError(
                    {"error": "Something went wrong, while doing image conversion"}
                )

        return super().retrieve(request, *args, **kwargs)

    @extend_schema(request=ImageUploadFinishedInputSerializer)
    @action(methods=["patch"], detail=True, url_path="upload-finished")
    def upload_finished(self, request, *args, **kwargs):
        """
        This endpoint will set image upload status to uploaded.
        If image not uploaded to s3, it will create a celery task to check after 5 mins
        """
        instance = self.get_object()

        # Update status if file exists
        if check_file_exists(instance.key):
            instance.status = UploadStatus.UPLOADED
            instance.save()
        else:
            # task will execute after 5 minutes to verify file uploaded
            process_image_upload.s(instance.id).apply_async(countdown=300)

        serializer = self.get_serializer(instance, many=False)
        return Response(serializer.data)
