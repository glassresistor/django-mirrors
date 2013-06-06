from django.contrib import admin
from . import models, forms

class SlugAdmin(admin.ModelAdmin):
    pass #form = forms.AssetForm
admin.site.register(models.Slug, SlugAdmin)

class AssetAdmin(admin.ModelAdmin):
    pass #form = forms.AssetForm
admin.site.register(models.Asset, AssetAdmin)

class ContentAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Content, ContentAdmin)

class ContentAttributeAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.ContentAttribute, ContentAttributeAdmin)

"""
class ListAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.List, ListAdmin)
"""

class ListMemberAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.ListMember, ListMemberAdmin)

