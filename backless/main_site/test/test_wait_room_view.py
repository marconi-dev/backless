from django.http.response import HttpResponse
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from main_site.models import Storage
from backless.settings import WS_URL


class WaitRoomViewTestCase(TestCase):
    ASSETS_DIR = 'main_site/test/testing_assets'

    def setUp(self):
        image = SimpleUploadedFile(
            name='astolfo.jpg',
            content=open(f'{self.ASSETS_DIR}/astolfo.jpg', 'rb').read(),
            content_type='image/jpeg')
        self.storage = Storage.objects.create(image=image)
        self.url = reverse("wait-room", kwargs={'pk': self.storage.id})
        self.response = self.client.get(self.url)
    
    def test_response_status_code_is_200(self):
        self.assertIsInstance(self.response, HttpResponse)
        self.storage.delete()

    def test_correct_template_is_returned(self):
        self.assertTemplateUsed(self.response, 'main_site/wait_room.html')
        self.storage.delete()
    
    def test_ws_url_is_correct(self):
        id = self.storage.id
        self.assertEqual(self.response.context['ws_url'], f"{WS_URL}/ws/wait/{id}")
        self.storage.delete()

