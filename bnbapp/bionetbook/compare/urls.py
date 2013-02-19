from django.conf.urls.defaults import patterns, url, include
from compare import views 
# from protocols import views

urlpatterns = patterns("",
    #url(regex=r'^(?P<protocol_slug>[-\w]+).svg$', view=protocol_plot, name='compare_protocol_plot'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.CompareBaseView.as_view(), name='compare_protocols'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareBaseGraphicView.as_view(), name='compare_protocol_graphic'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/layer/(?P<layers>[-\w]+)$', view=views.CompareLayersView.as_view(), name='add_layers'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/layer/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareLayersGraphicView.as_view(), name='add_layers_graphic'),

)
