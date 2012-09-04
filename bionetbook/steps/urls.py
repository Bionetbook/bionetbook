from django.conf.urls.defaults import patterns, url

from steps import views

urlpatterns = patterns("",

    url(regex=r'^new/$',
        view=views.StepCreateView.as_view(),
        name='step_create'),
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