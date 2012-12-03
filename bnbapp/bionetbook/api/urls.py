from django.conf.urls.defaults import patterns, url, include

from protocols import views

urlpatterns = patterns("",
	url(regex=r'^v1/protocol/(?P<protocol_slug>[-\w]+)$', view='api.views.protocol_detail', name='api_detail'),
)
