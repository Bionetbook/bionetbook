from django.conf.urls.defaults import patterns, url, include
from compare import views 
# from protocols import views

urlpatterns = patterns("",
    url(regex=r'^select/$', view=views.CompareSelectView.as_view(), name='compare_select'),

    url(regex=r'^view/single_ajax/(?P<protocol_a_slug>[-\w]+)/$', view=views.LayoutSingleView.as_view(), name='layout_sinlge_view'),
    url(regex=r'^clone/single_ajax/(?P<protocol_a_slug>[-\w]+)/$', view=views.CloneLayoutSingleView.as_view(), name='clone_layout_single_view'),

    url(regex=r'^view/ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.CompareDisplayView.as_view(), name='compare_display_view'),
    url(regex=r'^view/clone_ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.CloneDisplayView.as_view(), name='clone_display_view'),
    # url(regex=r'^view/clone_ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.CloneDisplayView.as_view(), name='clone_display_view'),

    # url(regex=r'^view/ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.AjaxView.as_view(), name='ajax_view'),

)


