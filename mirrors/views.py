from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from mirrors import models


def asset_media(request, slug):
    asset = get_object_or_404(models.Asset, slug=slug)
    response = HttpResponse(asset.data, mimetype=asset.get_encoding_display())
    response['Content-Disposition'] = 'inline; filename=%s'%slug
    return response
