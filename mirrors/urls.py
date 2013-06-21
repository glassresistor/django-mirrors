from django.conf.urls import patterns, url

from mirrors import views

urlpatterns = patterns('',
    url(r'^asset/media/(?P<slug>[-\w]+)/$', 
        views.asset_media, name='asset_media')
)
