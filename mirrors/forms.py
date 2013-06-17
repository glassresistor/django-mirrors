from django import forms
from django.core.files.base import ContentFile, File
from django.core.files.uploadedfile import UploadedFile
from mirrors import models, widgets, fields


class AssetForm(forms.ModelForm):

    data = fields.ByteaField()
    class Meta:
        model = models.Asset
