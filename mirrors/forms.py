from django import forms
from django.core.files.base import ContentFile, File
from django.core.files.uploadedfile import UploadedFile
from . import models, widgets


class AssetForm(forms.ModelForm):
    data = widgets.ByteaInput()
    def clean_data(self):
        return self.cleaned_data['data']

    class Meta:
        model = models.Asset
