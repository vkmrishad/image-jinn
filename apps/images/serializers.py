from django.utils.translation import ugettext_lazy as _

from drf_spectacular.utils import extend_schema_field
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.contrib.serializers import PresignedPostURLSerializer
from apps.contrib.storage import generate_presigned_post, generate_presigned_url
from apps.images.models import Image


class ImageSerializer(ModelSerializer):
    status = SerializerMethodField(read_only=True, help_text=_("Display status value"))
    presigned_url = SerializerMethodField(
        read_only=True, help_text=_("AWS S3 pre-signed image url")
    )

    class Meta:
        model = Image
        fields = ("id", "name", "mimetype", "status", "presigned_url", "message")

    def get_status(self, obj):
        return obj.get_status_display()

    @extend_schema_field(CharField)
    def get_presigned_url(self, obj):
        return generate_presigned_url(obj.key)

    @staticmethod
    def validate_name(name):
        if name:
            if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise ValidationError(
                    {"error": "Not a valid image format (.png, .jpg, .jpeg)"}
                )
        return name

    @staticmethod
    def validate_mimetype(mimetype):
        if mimetype:
            if not mimetype in ("image/jpg", ".image/jpeg", "image/png"):
                raise ValidationError(
                    {
                        "error": "Not a valid mimetype (image/jpg, .image/jpeg, image/png)"
                    }
                )
        return mimetype


class ImageUploadSerializer(ModelSerializer):
    status = SerializerMethodField(read_only=True, help_text=_("Display status value"))
    presigned_post_url = SerializerMethodField(
        read_only=True, help_text=_("AWS S3 pre-signed post url for upload")
    )
    presigned_url = SerializerMethodField(
        read_only=True, help_text=_("AWS S3 pre-signed image url")
    )

    class Meta:
        model = Image
        fields = (
            "id",
            "name",
            "mimetype",
            "status",
            "presigned_post_url",
            "presigned_url",
            "message",
        )

    def get_status(self, obj):
        return obj.get_status_display()

    @extend_schema_field(PresignedPostURLSerializer)
    def get_presigned_post_url(self, obj):
        return PresignedPostURLSerializer(
            generate_presigned_post(obj.key), many=False
        ).data

    @extend_schema_field(CharField)
    def get_presigned_url(self, obj):
        return generate_presigned_url(obj.key)

    @staticmethod
    def validate_name(name):
        if name:
            if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                raise ValidationError(
                    {"error": "Not a valid image format (.png, .jpg, .jpeg)"}
                )
        return name

    @staticmethod
    def validate_mimetype(mimetype):
        if mimetype:
            if not mimetype in ("image/jpg", ".image/jpeg", "image/png"):
                raise ValidationError(
                    {
                        "error": "Not a valid mimetype (image/jpg, .image/jpeg, image/png)"
                    }
                )
        return mimetype


class ImageUploadFinishedInputSerializer(Serializer):
    pass
