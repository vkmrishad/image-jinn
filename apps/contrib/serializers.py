from rest_framework.fields import CharField, URLField, DictField
from rest_framework.serializers import ModelSerializer, Serializer


class PresignedPostURLSerializer(Serializer):
    url = URLField()
    fields = DictField(child=CharField())
