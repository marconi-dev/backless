from django.forms import ModelForm
from .models import Storage


class StorageForm(ModelForm):
    class Meta:
        model = Storage
        fields = ['image']

