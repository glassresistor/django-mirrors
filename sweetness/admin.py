from django.contrib import admin
from . import models, forms


class AssetAdmin(admin.ModelAdmin):
    form = forms.AssetForm
admin.site.register(models.Asset, AssetAdmin)

class ExtendedContentAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.ExtendedContent, ExtendedContentAdmin)

class ArticleAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Article, ArticleAdmin)
