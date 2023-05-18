from django.http import JsonResponse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from main_site.models import Storage


class RemoveBackgroundTaskTestCase(TestCase):
    ASSETS_DIR = 'main_site/test/testing_assets'
    url = reverse('bg-remove-task')

    def setUp(self):
        self.image = SimpleUploadedFile(
            name='astolfo.jpg',
            content=open(f'{self.ASSETS_DIR}/astolfo.jpg', 'rb').read(),
            content_type='image/jpeg')
    
    def test_url_name(self):
        self.assertEqual(self.url, '/_tasks/remove-background/')

    def test_remove_background_task(self):
        id = Storage.objects.create(image=self.image).id
        kwargs = {"data": id, "content_type": "application/json"}
        response = self.client.post(self.url, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        Storage.objects.first().delete()

