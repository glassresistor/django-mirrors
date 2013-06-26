import json

from django.db.models import get_model

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from mirrors import models
from mirrors.api import fields as api_fields


class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data

        return super(MultipartResource, self).deserialize(request, data, format)


class PolymorphicRelatedField(fields.ToOneField):
        
    def get_related_resource(self, related_instance):
        """
        Instaniates the related resource.
        """

        to = {
            models.Slug: SlugResource,
            models.Asset: AssetResource,
            models.Content: ContentResource,
        }
        related_model = get_model(related_instance._meta.app_label, 
                           related_instance.__class__.__name__)
        related_resource = to[related_model]()
        # Fix the ``api_name`` if it's not present.
        if related_resource._meta.api_name is None:
            if self._resource and not self._resource._meta.api_name is None:
                related_resource._meta.api_name = self._resource._meta.api_name

        # Try to be efficient about DB queries.
        related_resource.instance = related_instance
        return related_resource


class MetaDataMixin(object):
    def dehydrate_metadata(self, bundle):
        return bundle.obj.metadata


class AssetResource(MultipartResource, MetaDataMixin, ModelResource):
    data = api_fields.ByteaField(attribute='data')
    data_url = fields.CharField(attribute='data_url', readonly=True)

    def deserialize(self, request, data, format=None):
        data = super(AssetResource, self).deserialize(request, data, format)
        data['data'] = buffer(data['data'].read())
        return data


    class Meta:
        queryset = models.Asset.objects.all()
        resource_name = 'asset'
        authorization= Authorization()
        excludes = ['data']


class SlugResource(ModelResource):

    class Meta:
        queryset = models.Slug.objects.all()
        resource_name = 'slug'
                

class ContentAttributeResource(MetaDataMixin, ModelResource):
    attribute = PolymorphicRelatedField(SlugResource, 'attribute',full=True)
    class Meta:
        queryset = models.ContentAttribute.objects.all()
        resource_name = 'contentattribute'
        authorization= Authorization()


class ListMemberResource(ModelResource):
    member = PolymorphicRelatedField(SlugResource, 'member',full=True)
    class Meta:
        queryset = models.ListMember.objects.all()
        resource_name = 'listmember'
        authorization= Authorization()


class ContentResource(MetaDataMixin, ModelResource):
    attributes = fields.ToManyField(ContentAttributeResource,
                attribute=lambda bundle: models.ContentAttribute.objects.filter(
                    parent=bundle.obj
                ), full=True, null=True)
    members = fields.ToManyField(ListMemberResource,
                attribute=lambda bundle: models.ListMember.objects.filter(
                    list=bundle.obj
                ), full=True, null=True)

    def dehydrate(self, bundle):
        mdict = {}
        for attribute in bundle.data['attributes']:
            mdict[attribute.data['keyword']] = attribute
        bundle.data['attributes'] = mdict
        return bundle
    
    
    class Meta:
        queryset = models.Content.objects.all()
        resource_name = 'content'
        authorization= Authorization()
