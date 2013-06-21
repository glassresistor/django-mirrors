from StringIO import StringIO
from PIL import Image

from django.test import TestCase
from django.test.client import RequestFactory

from mirrors import forms

class AssetSaveTest(TestCase):
    def test_asset_save(self):
        """
        Tests saving assets through the asset form(for admin mostly)
        """
        factory = RequestFactory()

        file_obj = StringIO()
        image = Image.new("RGBA", size=(50,50), color=(256,0,0))
        image.save(file_obj, 'png')
        file_obj.name = 'test.png'
        file_obj.seek(0)

        request = factory.post('/', {
            'slug': 'test', 
            'encoding': '.jpg',
            'metadata': '{}',
            'data': file_obj
        })
        form = forms.AssetForm(request.POST, request.FILES)
        asset = form.save()
        file_obj.seek(0)
        self.assertEqual(asset.data, file_obj.read())
