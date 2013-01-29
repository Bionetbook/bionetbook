from django.conf.urls.defaults import patterns, url, include

from protocols import views

urlpatterns = patterns("",

    url(regex=r'^$', view=views.ProtocolListView.as_view(), name='protocol_list'),

    # PROTOCOL URLS
    url(regex=r'^(?P<owner_slug>[-\w]+)/create/$', view=views.ProtocolCreateView.as_view(), name='protocol_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/$', view=views.ProtocolDetailView.as_view(), name='protocol_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/edit/$', view=views.ProtocolUpdateView.as_view(), name='protocol_update'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/publish/$', view=views.ProtocolPublishView.as_view(), name='protocol_publish'),

    # NODE
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<node_slug>[-\w]+)/delete/$', view=views.NodeDeleteView.as_view(), name='node_delete'),

    # STEP URLS
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/add-step/$', view=views.StepCreateView.as_view(), name='step_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/$', view=views.StepDetailView.as_view(), name='step_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/edit/$', view=views.StepUpdateView.as_view(), name='step_update'),

    # ACTION URLS
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/add-action/$', view=views.ActionVerbListView.as_view(), name='action_verb_list'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/add-action/(?P<verb_slug>[-\w]+)/$', view=views.ActionCreateView.as_view(), name='action_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/$', view=views.ActionDetailView.as_view(), name='action_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/edit/$', view=views.ActionUpdateView.as_view(), name='action_update'),

    # COMPONENT
    url(regex=r'^(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/(?P<component_slug>[-\w]+)/$', view=views.ActionDetailView.as_view(), name='component_detail'),
)
