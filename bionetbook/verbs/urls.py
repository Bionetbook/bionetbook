from django.conf.urls.defaults import patterns, url

from verbs import views

urlpatterns = patterns("",

    url(regex=r'^(?P<slug>[-\w]+)/$',
        view=views.VerbView.as_view(),
        name='verb_detail'),

)