from django.conf.urls.defaults import patterns, url

from protocols import views

urlpatterns = patterns("",

    url(regex=r'^new/$',
        view=views.ProtocolCreateView.as_view(),
        name='protocol_create'),
    url(regex=r'^(?P<slug>[-\w]+)/$',
        view=views.ProtocolDetailView.as_view(),
        name='protocol_detail'),
    url(regex=r'^(?P<slug>[-\w]+)/edit/$',
        view=views.ProtocolUpdateView.as_view(),
        name='protocol_update'),        
    url(regex=r'^$',
        view=views.ProtocolListView.as_view(),
        name='protocol_list'),
)