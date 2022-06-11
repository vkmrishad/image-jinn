from uuid import uuid4

from django.utils.translation import ugettext_lazy as _
from django.db.models import Model, UUIDField, DateTimeField


class BaseModel(Model):
    id = UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False,
        help_text=_("Using UUID instead of number"),
    )
    created_at = DateTimeField(
        auto_now_add=True, editable=False, help_text=_("Created time")
    )
    updated_at = DateTimeField(
        auto_now=True, editable=False, help_text=_("Updated time")
    )

    class Meta:
        abstract = True
