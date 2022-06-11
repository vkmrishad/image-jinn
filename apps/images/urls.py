from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from apps.images import views

router = routers.DefaultRouter()
router.register("", views.ImageViewSet)

urlpatterns = [
    path(r"", include(router.urls)),
    url(
        r"upload",
        views.ImageUploadViewSet.as_view({"post": "create"}),
        name="image-upload",
    ),
]
