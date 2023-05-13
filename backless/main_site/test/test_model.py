from django.test import TestCase
from main_site.models import Storage
from backless.settings import MEDIA_URL
from django.core.files.uploadedfile import SimpleUploadedFile


class StorageTestCase(TestCase):
    def setUp(self):
        self.ASSETS_DIR = 'main_site/test/testing_assets'
        self.images_data = [
            {
                'name':         'astolfo.jpg',
                'content_type': 'image/jpeg'
            },{
                'name':         'garvield.webp',
                'content_type': 'image/webp'
            },{
                'name':         'irelha.png',
                'content_type': 'image/png'
            },{
                'name':         'mexendinha_uwu.gif',
                'content_type': 'image/gif'
            }]
        self.images = [
            SimpleUploadedFile(
                name=data["name"],
                content=open(f'{self.ASSETS_DIR}/{data["name"]}', 'rb').read(),
                content_type=data["name"]
            ) for data in self.images_data ]

    
    def test_storage_was_successfuly_created(self):
        storage = Storage.objects.create(image=self.images[0]) 
        self.assertEqual(storage.image.name, 'astolfo.jpg')
        self.assertEqual(storage.image.url, f'{MEDIA_URL}astolfo.jpg')
        self.assertEqual(Storage.objects.count(), 1)
        storage.delete()

    def test_storage_background_remove(self):
        storage = Storage.objects.create(image=self.images[0]) 
        storage.remove_background()
        self.assertEqual(storage.image.name, 'astolfo.jpg.png')
        self.assertEqual(storage.image.url, f'{MEDIA_URL}astolfo.jpg.png')
        storage.delete()

    def test_background_remove_for_various_image_types(self):
        storages = [Storage(image=img_file) for img_file in self.images]
        Storage.objects.bulk_create(storages)
        self.assertEqual(Storage.objects.count(), 4) 

        for storage in Storage.objects.iterator():
            storage.remove_background()
            storage.delete()

