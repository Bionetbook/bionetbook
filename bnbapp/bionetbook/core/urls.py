from django.conf.urls.defaults import patterns, url

from core import views

urlpatterns = patterns("",
    url(regex=r'^dashboard/$', view=views.DashboardView.as_view(), name='dashboard'),
    url(regex=r'^tos/$', view=views.DashboardView.as_view(), name='tos'),
    url(regex=r'^privacy/$', view=views.DashboardView.as_view(), name='privacy'),
)
