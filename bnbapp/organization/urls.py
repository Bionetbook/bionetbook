from django.conf.urls.defaults import patterns, url, include
from organization import views

urlpatterns = patterns("",
    # url(regex=r'^$', view=views.OrganizationListView.as_view(), name='organization_list'),
    # url(regex=r'^(?P<slug>[-_\w]+)/$', view=views.OrganizationDetailView.as_view(), name='organization_detail'),
    url(regex=r'^(?P<owner_slug>[-\w]+)/$', view=views.OrganizationMainView.as_view(), name='organization_main'),
)
