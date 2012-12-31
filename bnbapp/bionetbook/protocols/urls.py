from django.conf.urls.defaults import patterns, url, include

from protocols import views

urlpatterns = patterns("",

    url(regex=r'^$', view=views.ProtocolListView.as_view(), name='protocol_list'),

    # PROTOCOL URLS
    url(regex=r'^create/$', view=views.ProtocolCreateView.as_view(), name='protocol_create'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/$', view=views.ProtocolDetailView.as_view(), name='protocol_detail'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/edit/$', view=views.ProtocolUpdateView.as_view(), name='protocol_update'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/publish/$', view=views.ProtocolPublishView.as_view(), name='protocol_publish'),

    # STEP URLS
    url(regex=r'^(?P<protocol_slug>[-\w]+)/add-step/$', view=views.StepCreateView.as_view(), name='step_create'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/$', view=views.StepDetailView.as_view(), name='step_detail'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/update/$', view=views.StepUpdateView.as_view(), name='step_update'),

    # ACTION URLS
    url(regex=r'^(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/add-action/$', view=views.ActionVerbListView.as_view(), name='action_verb_list'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/add-action/(?P<verb_slug>[-\w]+)/$', view=views.ActionCreateView.as_view(), name='action_create'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/$', view=views.ActionDetailView.as_view(), name='action_detail'),
    url(regex=r'^(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/update/$', view=views.ActionUpdateView.as_view(), name='action_update'),
)
