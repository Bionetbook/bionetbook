from django.conf.urls.defaults import patterns, url

from profiletools import views

from profiles.views import ProfileUpdateView

urlpatterns = patterns("",
    url(regex=r'^$',
        view=views.LoginRequireProfileListView.as_view(),
        name='profile_list'),
    url(regex=r'^mine/$',
        view=ProfileUpdateView.as_view(),
        name='profile_update'),
    url(regex=r'^(?P<pk>\d+)/$',
        view=views.ProfileDetailView.as_view(),
        name='profile_detail'),
)
