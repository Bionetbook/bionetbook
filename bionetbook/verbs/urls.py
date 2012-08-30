from django.conf.urls.defaults import patterns, url

from verbs import views

urlpatterns = patterns("",

    url(regex=r'^(?P<slug>[-\w]+)/$',
        view=views.VerbDetailView.as_view(),
        name='verb_detail'),
    url(regex=r'^$',
        view=views.VerbListView.as_view(),
        name='verb_list'),

)