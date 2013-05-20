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
    data = models.BinaryField()
    metadata = JSONField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)


class Content(models.Model):
    """
    Model for collections of content, most all types will work this way.
    """
    assets = models.ManyToManyField(Asset, through='ContentAttribute')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    metadata = JSONField()
    spec = models.CharField(max_length=10,
                            choices=(('article', 'Article',),
                                     ('page', 'Page',),
                                    ))


class ContentAttribute(models.Model):
    """
    Model for relating Content back to Assets.
    """
    metadata_override = JSONField()
    keyword = models.CharField(max_length=20)
    content = models.ForeignKey(Content)
    asset = models.ForeignKey(Asset)


class List(models.Model):
    """
    Model of list names.
    """
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField()
    members = models.ManyToManyField(Content, through='ListMember')


class ListMember(models.Model):
    """
    Ordered through model for List to Content
    """    
    list = models.ForeignKey(List)
    content = models.ForeignKey(Content)
    order = models.BigIntegerField(unique=True)
    
    class Meta:
        ordering = ('-order', 'list', 'content')
