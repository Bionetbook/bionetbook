from django.conf.urls.defaults import patterns, url

from core import views

urlpatterns = patterns("",

    url(regex=r'^$',
        view=views.DashboardView.as_view(),
        name='dashboard'),

)
