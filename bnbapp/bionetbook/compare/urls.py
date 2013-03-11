from django.conf.urls.defaults import patterns, url, include
from compare import views 
# from protocols import views

urlpatterns = patterns("",
    url(regex=r'^select/$', view=views.CompareSelectView.as_view(), name='compare_select'),

    #url(regex=r'^(?P<protocol_slug>[-\w]+).svg$', view=protocol_plot, name='compare_protocol_plot'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.CompareBaseView.as_view(), name='compare_protocols'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareBaseGraphicView.as_view(), name='compare_protocol_graphic'),
    # single protocols:
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/layers/(?P<layers>[-\w]+)/$', view=views.CompareSingleLayersView.as_view(), name='compare_single_layers'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/layers/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareSingleLayersGraphicView.as_view(), name='compare_single_layers_graphic'),
    # Double protocols
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/layers/(?P<layers>[-\w]+)/$', view=views.CompareLayersView.as_view(), name='compare_layers'),
    url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/layers/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareLayersGraphicView.as_view(), name='compare_layers_graphic'),
    
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/base/single/(?P<layers>[-\w]+)/$', view=views.SingleBaseView.as_view(), name='draw_single_base'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/base/single/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.SingleBaseGraphicView.as_view(), name='draw_single_base_graphic')

)


