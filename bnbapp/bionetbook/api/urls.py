from django.conf.urls.defaults import patterns, url, include

from protocols import views

urlpatterns = patterns("",
    url(regex=r'^(?P<protocol_slug>[-\w]+)/$', view=views.ProtocolDetailView.as_view(), name='api_detail'),
)