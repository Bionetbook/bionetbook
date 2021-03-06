from django.conf.urls.defaults import patterns, url

from core import views

urlpatterns = patterns("",
    url(regex=r'^dashboard/$', view=views.DashboardView.as_view(), name='dashboard'),
    url(regex=r'^tos/$', view=views.DashboardView.as_view(), name='tos'),
    url(regex=r'^privacy/$', view=views.DashboardView.as_view(), name='privacy'),
    url(regex=r'^documentation/$', view=views.DocumentationView.as_view(), name='documentation'),
    url(regex=r'^faq/$', view=views.FAQView.as_view(), name='faq'),
    url(regex=r'^release_notes/$', view=views.ReleaseNotes.as_view(), name='release_notes'),
)
