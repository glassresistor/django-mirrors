from tastypie import fields
from tastypie.resources import ModelResource
from mirrors import models


class AssetResource(ModelResource):

    class Meta:
        queryset = models.Asset.objects.all()
        resource_name = 'asset'


class ContentAttributeResource(ModelResource):
    asset = fields.ToOneField(AssetResource, 'asset',full=True)
    class Meta:
        queryset = models.ContentAttribute.objects.all()
        resource_name = 'contentattribute'


class ContentResource(ModelResource):
    assets = fields.ToManyField(ContentAttributeResource,
                attribute=lambda bundle: bundle.obj.assets.through.objects.filter(
                    content=bundle.obj) or bundle.obj.assets, full=True)

    """
    def dehydrate(self, bundle):
        data = bundle.data
        attrs = data['assets']
        for attr in attrs:
            attr_dict = attr.data
            asset = attr_dict
            data[asset['keyword']] = asset['asset']
        del bundle.data['assets']
        return bundle
    
    
    def hydrate(self, bundle):
        #TODO add unpack for keywords
        return bundle
    
    def build_schema(self):
        schema = super(ContentResource,self).build_schema()
        return schema
    """
    
    class Meta:
        queryset = models.Content.objects.all()
        resource_name = 'content'


class ListMemberResource(ModelResource):
    content = fields.ToOneField(ContentResource, 'content',full=True)
    class Meta:
        queryset = models.ListMember.objects.all()
        resource_name = 'listmember'


class ListResource(ModelResource):
    members = fields.ToManyField(ListMemberResource,
            attribute=lambda bundle: bundle.obj.members.through.objects.filter(
            list=bundle.obj) or bundle.obj.members, full=True)

    class Meta:
        queryset = models.List.objects.all()
        resource_name = 'list'
