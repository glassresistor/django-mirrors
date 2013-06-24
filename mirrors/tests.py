from django.core.urlresolvers import reverse
from StringIO import StringIO
from PIL import Image

from django.test import TestCase
from django.test.client import RequestFactory
from tastypie.test import ResourceTestCase
from mirrors import forms, models


def build_fake_image():
    file_obj = StringIO()
    image = Image.new("RGBA", size=(50,50), color=(256,0,0))
    image.save(file_obj, 'png')
    file_obj.name = 'test.png'
    file_obj.seek(0)
    return file_obj


def build_request_dict(file_obj):
    return {
        'slug': 'test', 
        'encoding': '.jpg',
        'metadata': '{}',
        'data': file_obj
    }


class AssetSaveTest(ResourceTestCase): #ugh subclassing for asserts...
    def assert_file_equals(self, data, file_obj):
        file_obj.seek(0)
        self.assertEqual(data, file_obj.read())

    def assert_asset_same(self, req_dict, asset):
        req_dict['metadata'] = {}
        del req_dict['data']
        for key, value in req_dict.iteritems():
            self.assertEqual(value, getattr(asset, key))

    def test_asset_form_save(self):
        """
        Tests saving assets through the asset form(for admin mostly)
        """
        factory = RequestFactory()
        file_obj = build_fake_image()
        req_dict = build_request_dict(file_obj)
        request = factory.post('/', req_dict)
        form = forms.AssetForm(request.POST, request.FILES)
        asset = form.save()
        self.assert_file_equals(asset.data, file_obj)
        self.assert_asset_same(req_dict, asset)
        
    def test_asset_api_post(self):
        url = reverse('api_dispatch_list', kwargs={
            'resource_name': 'asset', 'api_name': 'v1'
            })
        file_obj = build_fake_image()
        request = build_request_dict(file_obj)
        self.client.post(url, data=request)
        asset = models.Asset.objects.get(slug=request['slug'])
        self.assert_file_equals(asset.data, file_obj)
        self.assert_asset_same(request, asset)
        
        
