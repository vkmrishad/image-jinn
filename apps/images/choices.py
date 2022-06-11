from django.db.models import IntegerChoices
from django.utils.translation import ugettext_lazy as _


class UploadStatus(IntegerChoices):
    UPLOADING = 1, _("Uploading")
    UPLOADED = 2, _("Uploaded")
    PROCESSING = 3, _("Processing")
    PROCESSED = 4, _("Processed")
    ERROR = 5, _("Error")
