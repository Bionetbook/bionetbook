from django.conf.urls.defaults import patterns, url, include

from protocols import views
import compare.views as cviews

urlpatterns = patterns("",

    url(regex=r'^protocols/$', view=views.ProtocolListView.as_view(), name='protocol_list'),
    # url(regex=r'^protocols/(?P<protocol_a_slug>[-\w]+)/layers/(?P<layers>[-\w]+)/$', view=cviews.CompareSingleLayersView.as_view(), name='draw_single_layers'),
    # PROTOCOL URLS
    url(regex=r'^(?P<owner_slug>[-\w]+)/$', view=views.ProtocolListView.as_view(), name='organization_protocol_list'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/create/$', view=views.ProtocolCreateView.as_view(), name='protocol_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/$', view=views.ProtocolDetailView.as_view(), name='protocol_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/edit/$', view=views.ProtocolUpdateView.as_view(), name='protocol_update'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/publish/$', view=views.ProtocolPublishView.as_view(), name='protocol_publish'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/duplicate/$', view=views.ProtocolDuplicateView.as_view(), name='protocol_duplicate'),

    # STEP URLS
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/add-step/$', view=views.StepCreateView.as_view(), name='step_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/$', view=views.StepDetailView.as_view(), name='step_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/edit/$', view=views.StepUpdateView.as_view(), name='step_update'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/delete/$', view=views.StepDeleteView.as_view(), name='step_delete'),

    # ACTION URLS
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/add-action/$', view=views.ActionVerbListView.as_view(), name='action_verb_list'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/add-action/(?P<verb_slug>[-\w]+)/$', view=views.ActionCreateView.as_view(), name='action_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/$', view=views.ActionDetailView.as_view(), name='action_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/edit/$', view=views.ActionUpdateView.as_view(), name='action_update'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/delete/$', view=views.ActionDeleteView.as_view(), name='action_delete'),

    # MACHINE
    # url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/add-machine/$', view=views.MachineCreateView.as_view(), name='machine_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/(?P<machine_slug>[-\w]+)/$', view=views.MachineDetailView.as_view(), name='machine_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/(?P<machine_slug>[-\w]+)/edit/$', view=views.MachineUpdateView.as_view(), name='machine_edit'),
    # url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/machine/delete/$', view=views.MachineDeleteView.as_view(), name='machine_delete'),

    # COMPONENT
    # url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/add-component/$', view=views.ComponentCreateView.as_view(), name='component_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/c/(?P<component_slug>[-\w]+)/$', view=views.ComponentDetailView.as_view(), name='component_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/c/(?P<component_slug>[-\w]+)/edit/$', view=views.ComponentUpdateView.as_view(), name='component_edit'),
    # url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/c/(?P<component_slug>[-\w]+)/delete/$', view=views.ComponentDeleteView.as_view(), name='component_delete'),

    # THERMOCYCLER
    # url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/add-termocycler/$', view=views.ThermocyclerCreateView.as_view(), name='thermocycler_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/t/(?P<thermo_slug>[-\w]+)/$', view=views.ThermocyclerDetailView.as_view(), name='thermocycler_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/t/(?P<thermo_slug>[-\w]+)/edit/$', view=views.ThermocyclerUpdateView.as_view(), name='thermocycler_update'),
    # url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<protocol_slug>[-\w]+)/(?P<step_slug>[-\w]+)/(?P<action_slug>[-\w]+)/t/(?P<thermocycler_slug>[-\w]+)/delete/$', view=views.ThermocyclerDeleteView.as_view(), name='thermocycler_delete'),
)
