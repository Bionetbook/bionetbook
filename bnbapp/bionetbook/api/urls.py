from django.conf.urls.defaults import patterns, url, include

from protocols import views

urlpatterns = patterns("",
    url(regex=r'^(?v1/P<component>[-\w]+)/P<protocol_slug>[-\w]+)/$', view=views.ProtocolDetailView.as_view(), name='api_detail'),
)