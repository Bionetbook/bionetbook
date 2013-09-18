from django.conf.urls.defaults import patterns, url, include
from schedule import views

urlpatterns = patterns("",
    url(regex=r'^create/$', view=views.CalendarCreateView.as_view(), name='create_calendar'),
    url(regex=r'^(?P<pk>[-\w]+)/$', view=views.ScheduleAPI.as_view(), name='single_calendar'),
    url(r'^$', view=views.CalendarListView.as_view(), name='calendar_list')
)