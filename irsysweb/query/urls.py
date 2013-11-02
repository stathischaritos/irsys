# app specific urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse


urlpatterns = patterns('',
    url(r'^home', 'query.views.home'),
)
