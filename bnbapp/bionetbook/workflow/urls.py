from django.conf.urls.defaults import patterns, url, include
from workflow import views

urlpatterns = patterns("",
    url(regex=r'^(?P<owner_slug>[-\w]+)/workflows/create/$', view=views.WorkflowCreateView.as_view(), name='workflow_create'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/workflows/(?P<workflow_slug>[-\w]+)/$', view=views.WorkflowDetailView.as_view(), name='workflow_detail'),

    #url(regex=r'^(?P<owner_slug>[-\w]+)/$', view=views.WorkflowListView.as_view(), name='workflow_list'),
    #url(regex=r'^(?P<owner_slug>[-\w]+)/add/$', view=views.WorkflowCreateView.as_view(), name='workflow_create'),
    #url(regex=r'^(?P<owner_slug>[-\w]+)/workflows/(?P<pk>[-\w]+)/$', view=views.WorkflowDetailView.as_view(), name='workflow_detail'),
    #url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<workflow_slug>[-\w]+)/edit/$', view=views.WorkflowUpdateView.as_view(), name='workflow_update'),
    #url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<workflow_slug>[-\w]+)/delete/$', view=views.WorkflowDeleteView.as_view(), name='workflow_delete'),
)
