from django.utils.translation import ugettext_lazy as _
from django.db.models import TextField, CharField, PositiveSmallIntegerField

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
    message = TextField(null=True, blank=True, help_text=_("Error messages, if any"))

    @property
    def key(self):
        ext = self.name.split(".")[-1]
        return f"images/{self.id}/image-{self.id}.{ext}"

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.key
