from django.conf.urls.defaults import patterns, url, include

from protocols import views

urlpatterns = patterns("",
    url(regex=r'^(?P<protocol_slug>[-\w]+).svg$', view=views.protocol_plot(), name='compare_protocol_plot'),
)
