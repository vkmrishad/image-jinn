from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.db.models import TextField, CharField, PositiveSmallIntegerField, JSONField

from apps.contrib.models import BaseModel
from apps.images.choices import UploadStatus


class Image(BaseModel):
    mimetype = CharField(max_length=100, help_text=_("Image mimetype"))
    name = CharField(max_length=250, help_text=_("Original file name"))
    status = PositiveSmallIntegerField(
        choices=UploadStatus.choices,
        default=UploadStatus.UPLOADING,
        help_text=_("Image upload status"),
    )
    available_extensions = ArrayField(
        default=list,
        base_field=CharField(
            max_length=25, help_text="Image format like png, jpg, jpeg, etc"
        ),
        help_text=_("Store available extensions as a Array/List"),
    )
    message = TextField(null=True, blank=True, help_text=_("Error messages, if any"))

    @property
    def key(self):
        ext = self.name.split(".")[-1]
        return f"images/{self.id}/image-{self.id}.{ext}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.key
