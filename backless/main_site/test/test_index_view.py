from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from main_site.models import Storage
from django.test import TestCase


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.ASSETS_DIR = 'main_site/test/testing_assets'
        self.image = SimpleUploadedFile(
            name='astolfo.jpg',
            content=open(f'{self.ASSETS_DIR}/astolfo.jpg', 'rb').read(),
            content_type='image/jpeg')
    

    def test_request_get_success(self):
        response = self.client.get('/')
        self.assertIsInstance(response, HttpResponse)

    def test_request_post_success(self):
        response = self.client.post('/', data={'image': self.image})
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, '/wait/')
        Storage.objects.first().delete()

    def test_request_post_fail(self):
        response = self.client.post('/', data={'wrong-field': self.image})
        self.assertIsInstance(response, TemplateResponse)

    def test_request_post_form_invalid(self):
        response = self.client.post('/', data={'image': 'hello'})
        self.assertIsInstance(response, TemplateResponse)

