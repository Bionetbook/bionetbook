from django.conf.urls.defaults import patterns, url, include
from interest import views

urlpatterns = patterns("",
    url(r'^$', views.InterestCreate.as_view(), name='interest_signup'),
)
