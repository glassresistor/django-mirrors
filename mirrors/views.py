from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

from mirrors import models


@never_cache
def asset_media(request, slug):
    asset = get_object_or_404(models.Asset, slug=slug)
    response = HttpResponse(asset.data, mimetype=asset.mimetype)
    response['Content-Disposition'] = 'inline; filename=%s'%slug
    return response
