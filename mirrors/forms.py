from django import forms
from django.core.files.base import ContentFile, File
from django.core.files.uploadedfile import UploadedFile
from . import models, widgets


class AssetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(AssetForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        return super(AssetForm, self).save(*args, **kwargs)
        
    class Meta:
        model = models.Asset
        widgets = {
            'data': widgets.ByteaInput(),
        }
