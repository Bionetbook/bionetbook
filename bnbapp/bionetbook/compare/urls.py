from django.conf.urls.defaults import patterns, url, include
from compare import views 
# from protocols import views

urlpatterns = patterns("",
    #url(regex=r'^(?P<protocol_slug>[-\w]+).svg$', view=protocol_plot, name='compare_protocol_plot'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.CompareBaseView.as_view(), name='compare_protocols'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareBaseGraphicView.as_view(), name='compare_protocol_graphic'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/layers/(?P<layers>[-\w]+)/$', view=views.CompareLayersView.as_view(), name='add_layers'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/layers/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareLayersGraphicView.as_view(), name='add_layers_graphic'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/layers/(?P<layers>[-\w]+)/$', view=views.SingleLayersView.as_view(), name='add_single_layers'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/layers/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.SingleLayersGraphicView.as_view(), name='add_single_layers_graphic')
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/base/single/(?P<layers>[-\w]+)/$', view=views.SingleBaseView.as_view(), name='draw_single_base'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/base/single/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.SingleBaseGraphicView.as_view(), name='draw_single_base_graphic')

)
