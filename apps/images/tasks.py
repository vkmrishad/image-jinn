from celery import shared_task
from celery.utils.log import get_task_logger

from apps.contrib.storage import check_file_exists
from apps.images.choices import UploadStatus
from apps.images.models import Image

logger = get_task_logger(__name__)


@shared_task(max_retries=3, name="apps.images.process_image_upload")
def process_image_upload(image_id):
    image = Image.objects.get(id=image_id)
    try:
        if check_file_exists(image.key):
            image.status = UploadStatus.UPLOADED
        else:
            image.status = UploadStatus.ERROR
            image.message = "Not Uploaded"
    except Exception as e:
        image.status = UploadStatus.ERROR
        image.message = str(e)
        logger.error("Upload Error", e, image_id)
    image.save()
