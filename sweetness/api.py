from tastypie import fields
from tastypie.resources import ModelResource
from . import models


class AssetResource(ModelResource):
    class Meta:
        queryset = models.Asset.objects.all()
        resource_name = 'asset'

class ArticleResource(ModelResource):
    body = fields.ForeignKey(AssetResource, 'body', full=True)
    
    class Meta:
        queryset = models.Article.objects.all()
        resource_name = 'article'
