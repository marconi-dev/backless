from backless.cloud_tasks import send_task
from .models import Storage
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save


@receiver(pre_delete, sender=Storage)
def delete_img_file_from_storage(instance, **kwargs):
    instance.image.delete()

@receiver(post_save, sender=Storage)
def trigger_task(instance, created, **kwargs):
    if created:
        send_task('_tasks/remove-background/', payload=str(instance.id))

