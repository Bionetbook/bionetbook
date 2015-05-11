from django.conf.urls.defaults import *

from feedback import views

urlpatterns = patterns('',
    url(r'^$', views.FeedbackView.as_view(), name='feedback-form'),
    url(r'^success/$', views.FeedbackSuccessView.as_view(), name='feedback-success'),
)
