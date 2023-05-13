from .models import Storage
from django.dispatch import receiver
from django.db.models.signals import pre_delete


@receiver(pre_delete, sender=Storage)
def delete_img_file_from_storage(instance, **kwargs):
    instance.image.delete()

