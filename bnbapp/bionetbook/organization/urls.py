from django.conf.urls.defaults import patterns, url, include
from organization import views

urlpatterns = patterns("",
    url(regex=r'^(?P<slug>[-_\w]+)/$', view=views.OrganizationDetailView.as_view(), name='organization_detail'),
)