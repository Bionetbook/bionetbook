from django.conf.urls.defaults import patterns, url

from profiletools import views

urlpatterns = patterns("",
    url(regex=r'^mine/$',
        view=views.DefaultProfileUpdateNoSlugView.as_view(),
        name='profile_update'),
    url(regex=r'^(?P<pk>\d+)/$',
        view=views.ProfileDetailView.as_view(),
        name='profile_detail'),
)
