from django.conf.urls.defaults import patterns, url, include
from compare import views 
# from protocols import views

urlpatterns = patterns("",
    url(regex=r'^select/$', view=views.CompareSelectView.as_view(), name='compare_select'),
    
    url(regex=r'^view/single_ajax/(?P<protocol_a_slug>[-\w]+)/$', view=views.AjaxSingleView.as_view(), name='ajax_sinlge_view'),
    url(regex=r'^view/ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.AjaxView.as_view(), name='ajax_view'),
    
    




    #url(regex=r'^(?P<protocol_slug>[-\w]+).svg$', view=protocol_plot, name='compare_protocol_plot'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.CompareBaseView.as_view(), name='compare_protocols'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareBaseGraphicView.as_view(), name='compare_protocol_graphic'),
    # single protocols:
    # !!! DEPRECATED !!!
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/layers/(?P<layers>[-\w]+)/$', view=views.CompareSingleLayersPyGvView.as_view(), name='compare_single_layers'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/layers/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareSingleLayersGraphicPyGvView.as_view(), name='compare_single_layers_graphic'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/$', view=views.CompareLayersView.as_view(), name='protocol_basic'),

    # Double protocols
    

    # !!! DEPRECATED !!!
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/layers/(?P<layers>[-\w]+)/$', view=views.CompareLayersPyGvView.as_view(), name='compare_layers'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/layers/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.CompareLayersGraphicPyGvView.as_view(), name='compare_layers_graphic'),
    
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/base/single/(?P<layers>[-\w]+)/$', view=views.SingleBaseView.as_view(), name='draw_single_base'),
    # url(regex=r'^(?P<protocol_a_slug>[-\w]+)/base/single/(?P<layers>[-\w]+).(?P<format>[-\w]+)$', view=views.SingleBaseGraphicView.as_view(), name='draw_single_base_graphic')

)


