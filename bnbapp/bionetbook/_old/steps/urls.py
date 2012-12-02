from django.conf.urls.defaults import patterns, url, include

from steps import views

urlpatterns = patterns("",

    url(regex=r'^new/$',
        view=views.StepCreateView.as_view(),
        name='step_create'),
    url(r'^(?P<step_slug>[-\w]+)/actions/', include('actions.urls')),
    url(regex=r'^(?P<slug>[-\w]+)/$',
        view=views.StepDetailView.as_view(),
        name='step_detail'),
    url(regex=r'^(?P<slug>[-\w]+)/edit/$',
        view=views.StepUpdateView.as_view(),
        name='step_update'),
    url(regex=r'^$',
        view=views.StepListView.as_view(),
        name='step_list'),
)