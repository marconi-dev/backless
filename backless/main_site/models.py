from rembg import remove 
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


# Create your models here.
class Storage(models.Model):
    image = models.ImageField()


    def __str__(self):
        return self.image.name

    @property
    def _img_data(self):
        with self.image.open() as img:
            return img.read()

    def remove_background(self):
        processed_img = remove(self._img_data)
        new_name = self.image.name + '.png'
        new_img = default_storage.save(new_name, ContentFile(processed_img))
        self.update_image(new_img)

    def update_image(self, new_img):
        self.image.delete()
        self.image = new_img
        self.save()

