from django.conf.urls.defaults import patterns, url, include
from workflow import views

urlpatterns = patterns("",
    url(regex=r'^(?P<owner_slug>[-\w]+)/$', view=views.WorkflowListView.as_view(), name='workflow_list'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<workflow_slug>[-\w]+)/$', view=views.WorkflowDetailView.as_view(), name='workflow_detail'),
    #url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<workflow_slug>[-\w]+)/edit/$', view=views.ProtocolUpdateView.as_view(), name='protocol_update'),
    #url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<workflow_slug>[-\w]+)/publish/$', view=views.ProtocolPublishView.as_view(), name='protocol_publish'),
    #url(regex=r'^(?P<owner_slug>[-\w]+)/(?P<workflow_slug>[-\w]+)/duplicate/$', view=views.ProtocolDuplicateView.as_view(), name='protocol_duplicate'),
)


