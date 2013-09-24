from django.conf.urls.defaults import patterns, url, include

from experiment import views


urlpatterns = patterns("",

    # url(regex=r'^protocols/$', view=views.ProtocolListView.as_view(), name='protocol_list'),
    # url(regex=r'^protocols/(?P<protocol_a_slug>[-\w]+)/layers/(?P<layers>[-\w]+)/$', view=cviews.CompareSingleLayersView.as_view(), name='draw_single_layers'),
    # PROTOCOL URLS
    # url(regex=r'^(?P<owner_slug>[-\w]+)/workflows/create/$', view=wviews.WorkflowCreateView.as_view(), name='workflow_create'),
    # url(regex=r'^(?P<owner_slug>[-\w]+)/workflows/(?P<workflow_slug>[-\w]+)/$', view=wviews.WorkflowDetailView.as_view(), name='workflow_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/experiments/create/', view=views.ExperimentCreateView.as_view(), name='experiment_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/experiments/(?P<experiment_slug>[-\w]+)/edit/', view=views.ExperimentUpdateView.as_view(), name='experiment_update'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/experiments/(?P<experiment_slug>[-\w]+)/add/', view=views.ExperimentAddView.as_view(), name='experiment_add'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/experiments/(?P<experiment_slug>[-\w]+)/', view=views.ExperimentDetailView.as_view(), name='experiment_detail'),
)
