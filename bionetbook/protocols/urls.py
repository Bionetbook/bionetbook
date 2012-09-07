from django.conf.urls.defaults import patterns, url, include

from protocols import views

urlpatterns = patterns("",

    url(regex=r'^new/$',
        view=views.ProtocolCreateView.as_view(),
        name='protocol_create'),
    url(r'^(?P<protocol_slug>[-\w]+)/steps/', include('steps.urls')),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/$',
        view=views.ProtocolDetailView.as_view(),
        name='protocol_detail'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/edit/$',
        view=views.ProtocolUpdateView.as_view(),
        name='protocol_update'),
    url(regex=r'^$',
        view=views.ProtocolListView.as_view(),
        name='protocol_list'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/publish/$',
        view=views.ProtocolPublishView.as_view(),
        name='protocol_publish'),
)