from django import forms
from django.core.files.base import ContentFile, File
from django.core.files.uploadedfile import UploadedFile

from . import models

class AssetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #Clean this up it will get ugly.
        if len(args) > 0 and not args[1]:
            cf = ContentFile(args[0].get('data'))
            args = (args[0], {'data': UploadedFile(cf, args[0].get('slug') + '.md', size=cf.size)})
        super(AssetForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.files['data'].name = '%s.%s' % (
            self.cleaned_data['slug'], self.cleaned_data['encoding'])
        return super(AssetForm, self).save(*args, **kwargs)
        
    class Media:
        js = ('jquery_fix.js', 'js/jquery-1.9.1.js', 'js/jquery-ui-1.10.2.custom.js',
              'http://rangy.googlecode.com/svn/trunk/currentrelease/rangy-core.js',
              'hallo.js', 'editor.js',)
        css = {
                'all': ('css/ui-darkness/jquery-ui-1.10.2.custom.css',
                        'fontawesome/css/font-awesome.css',
                        )
              }
        
    class Meta:
        model = models.Asset
        widgets = {
            #'data': forms.HiddenInput,
        }
