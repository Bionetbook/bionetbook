from django.conf.urls.defaults import patterns, url, include

from protocols import views

urlpatterns = patterns("",
	url(regex=r'^v1/protocol/(?P<protocol_slug>[-\w]+)/$', view='api.views.protocol_detail', name='api_detail'),
)

#urlpatterns = patterns("",
#    url(regex=r'^(?v1/P<component>[-\w]+)/P<protocol_slug>[-\w]+)/$', view=views.ProtocolDetailView.as_view(), name='api_detail'),
#)