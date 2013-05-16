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

    def dehydrate(self, bundle):
        data = bundle.data
        attrs = data['assets']
        for attr in attrs:
            attr_dict = attr.data
            asset = attr_dict
            data[asset['keyword']] = asset['asset']
        del bundle.data['assets']
        return bundle
    
    class Meta:
        queryset = models.Content.objects.all()
        resource_name = 'content'


"""
class ArticleResource(ModelResource):
    body = fields.ForeignKey(AssetResource, 'body', full=True)
    
    class Meta:
        queryset = models.Article.objects.all()
        resource_name = 'article'
"""
