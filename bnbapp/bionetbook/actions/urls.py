from django.conf.urls.defaults import patterns, url

from actions import views

urlpatterns = patterns("",

    url(regex=r'^new/$',
        view=views.ActionCreateView.as_view(),
        name='action_create'),
    url(regex=r'^(?P<slug>[-\w]+)/$',
        view=views.ActionDetailView.as_view(),
        name='action_detail'),
    url(regex=r'^(?P<slug>[-\w]+)/edit/$',
        view=views.ActionUpdateView.as_view(),
        name='action_update'),
    url(regex=r'^$',
        view=views.ActionListView.as_view(),
        name='action_list'),
    url(regex=r'^ajax/(?P<action_pk>\d+)/(?P<verb_slug>[-\w]+)/$',
        view=views.ActionVerbAjaxView.as_view(),
        name='verb_ajax_form'),
)