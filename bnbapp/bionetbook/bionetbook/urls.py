from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, View

admin.autodiscover()

urlpatterns = patterns('',
    url(regex=r'^$', view=TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^test/', view=TemplateView.as_view(template_name="test1.svg"), name="test1"),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^', include('core.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^compare/', include('compare.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^signup/', include('interest.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login/'}, 'logout',),
    url(r'^', include('protocols.urls')),
    url(r'^', include('organization.urls')),
    url(r'^', include('workflow.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
else:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )
