import mimetypes
from model_utils.managers import InheritanceManager

from django.db import models
from django.core.exceptions import ValidationError
from jsonfield import JSONField

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from djorm_pgbytea.fields import ByteaField
from django.core.urlresolvers import reverse


class AutoInheritanceManager(InheritanceManager):
    def all(self, *subclasses):
        return self.select_subclasses(*subclasses)

    def get(self, *args, **kwargs):
        return self.get_subclass(*args, **kwargs)


class Slug(models.Model):
    """
    Core namespace of assets and contents.  A kludge to avoid content types.
    """
    objects = AutoInheritanceManager() #to make it polymorphic

    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.__class__.__name__, self.slug.replace('-',' ').title())


class Asset(Slug):
    """
    Core model for storing content text or binary with json encoded metadata.
    FileField abstraction offers easy alteration of storage backends.
    """
    encoding = models.CharField(max_length=5,
                            choices=mimetypes.types_map.items(),
                            default='.md')
    data = ByteaField(null=False)
    metadata = JSONField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    @property
    def data_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return reverse('asset_media', args=[self.slug])


class Content(Slug):
    """
    Model for collections of content, most all types will work this way.
    """
    metadata = JSONField()
    spec = models.CharField(max_length=10,
                            choices=(('article', 'Article',),
                                     ('page', 'Page',),
                                    ))
    is_published = models.BooleanField(default=False, null=False)

    def __unicode__(self):
        return u'%s: %s' % (self.spec.title(), self.slug.replace('-',' ').title())


class ContentAttribute(models.Model):
    """
    Model for relating Content back to Assets.
    """
    metadata = JSONField()
    keyword = models.CharField(max_length=20)
    parent = models.ForeignKey(Content, related_name='attributes')
    attribute = models.ForeignKey(Slug)

    class Meta:
        ordering = ('parent', 'keyword',)


class ListMember(models.Model):
    """
    Ordered through model for List to Content
    """    
    list = models.ForeignKey(Content, related_name='members')
    member = models.ForeignKey(Slug)
    order = models.BigIntegerField()
    
    class Meta:
        ordering = ('list', '-order',)
