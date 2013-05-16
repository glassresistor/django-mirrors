from django.contrib import admin
from . import models, forms


class AssetAdmin(admin.ModelAdmin):
    form = forms.AssetForm
admin.site.register(models.Asset, AssetAdmin)

class ContentAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Content, ContentAdmin)

class ContentAttributeAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.ContentAttribute, ContentAttributeAdmin)

