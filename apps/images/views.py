from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from apps.contrib.storage import check_file_exists
from apps.images.choices import UploadStatus
from apps.images.models import Image
from apps.images.tasks import process_image_upload
from apps.images.serializers import (
    ImageSerializer,
    ImageUploadFinishedInputSerializer,
    ImageUploadSerializer,
)


class ImageUploadViewSet(CreateModelMixin, GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        instance = super().create(request, *args, **kwargs)
        # task will execute after 5 minutes to verify file uploaded
        process_image_upload.s(instance.data.get("id")).apply_async(countdown=300)
        return instance


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "patch", "partial_update"]

    @extend_schema(request=ImageUploadFinishedInputSerializer)
    @action(methods=["patch"], detail=True, url_path="upload-finished")
    def upload_finished(self, request, *args, **kwargs):
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
