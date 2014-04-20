from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^nava/(?P<channel>[a-z\.]+)$', 'nava.views.home'),
)
