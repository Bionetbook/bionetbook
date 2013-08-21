from django.conf.urls.defaults import patterns, url, include
from schedule import views

urlpatterns = patterns("",
    url(r'^$', views.ScheduleAPI.as_view(), name='schedule_experiment')
)