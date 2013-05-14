from django.db import models
from django.core.exceptions import ValidationError
from jsonfield import JSONField
from tastypie.serializers import Serializer

from . import fields


class Asset(models.Model):
    """
    Core model for storing content text or binary with json encoded metadata.
    FileField abstraction offers easy alteration of storage backends.
    """
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    encoding = models.CharField(max_length=5,
                            choices=(('md', 'Markdown',),
                                     #('html', 'HTML',),
                                     ('png', 'Image(png)',),
                                    ),
                            default='md',)
    content = models.FileField(upload_to='content')
    metadata = JSONField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    

class ExtendedContent(models.Model):
    """
    Base model for collections of content to be used in building compiled 
    content.
    """
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    metadata = JSONField()
    
    def __init__(self, *args, **kwargs):
        super(ExtendedContent, self).__init__(*args, **kwargs)
              
    def render(self, context):
        raise NotImplemented("Not Implemented for %s" % self.__name__)

    def compile_src(self):
        dictionary = {}
        for field in self._meta.fields:
            value = getattr(self, field.name)
            if issubclass(field.__class__, fields.ContentField):
                item = {
                    'metadata': value.metadata, 
                    'content': value.content.url,
                }
            else:
                item = value
            dictionary[field.name] = item       
        return dictionary


class CompiledContent(models.Model):
    """
    Is the compiled version of ExtentedContent.
    """
    src = models.ForeignKey(ExtendedContent)
    build_date = models.DateTimeField(auto_now=True)
    json = JSONField()

    
class Article(ExtendedContent):
    """
    Test model for Articles.
    """
    body = fields.ContentField(encodings=['md','html'], 
                    required_fields=['title','description'])
    publish_date = models.DateTimeField()
    
