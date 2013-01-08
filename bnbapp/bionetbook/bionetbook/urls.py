from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',

    url(regex=r'^$',
        view=TemplateView.as_view(template_name="home.html"),
        name="home"
        ),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('core.urls')),
    url(r'^protocol/', include('protocols.urls')),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^signup/', include('interest.urls')),
    #url(r'^verbs/', include('verbs.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login/'}, 'logout',),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
