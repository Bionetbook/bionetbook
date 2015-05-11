from django.conf.urls.defaults import patterns, url, include

#from protocols import views
from api import views

urlpatterns = patterns("",
	# incomplete ajax:
	url(regex=r'^protocol/(?P<protocol_id>[-\d]+)/$', view=views.ProtocolAPI.as_view(), name='protocol_api'),			# TRY FOR THE ID FIRST
	url(regex=r'^protocol/(?P<protocol_slug>[-\w]+)/$', view=views.ProtocolAPI.as_view(), name='protocol_api_slug'),

	url(regex=r'^view/data_static/$', view=views.AjaxStaticView.as_view(), name='ajax_static_view'),
	
	url(regex=r'^json/data_dynamic/$', view='api.views.json_data_dynamic', name='json_data_dynamic'),
	url(regex=r'^view/ajax_dynamic/$', view=views.AjaxDynamicView.as_view(), name='ajax_dynamic_view'),
	
	url(regex=r'^json/single_ajax/(?P<protocol_a_slug>[-\w]+)/$', view=views.ProtocolLayoutAPI.as_view(), name='get_layout_json'),
	# url(regex=r'^view/single_ajax/(?P<protocol_a_slug>[-\w]+)/$', view=views.AjaxSingleView.as_view(), name='AjaxSinlgeView'),

	url(regex=r'^json/ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view='api.views.get_layout_compare_json', name='get_layout_compare_json'),
	url(regex=r'^json/clone_ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view='api.views.get_layout_clone_json', name='get_layout_clone_json'),
	# url(regex=r'^view/ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.AjaxView.as_view(), name='ajax_view'),
	url(regex=r'^calendar/$', view=views.ListCalendarAPI.as_view(), name='ListCalendarAPI'),
	url(regex=r'^calendar/(?P<pk>[-\w]+)/$', view=views.SingleCalendarAPI.as_view(), name='EventAPI'),
	url(regex=r'^calendar/(?P<pk>[-\w]+)/(?P<event_id>[-\w]+)/$', view=views.SingleEventAPI.as_view(), name='SingleEventAPI'),
	url(regex=r'^action/fields/(?P<slug>[-\w]+)/$', view=views.VerbFieldAPI.as_view(), name='api_verb_fields'),
	url(regex=r'^action/types/$', view='api.views.get_verb_types_json', name='api_verb_types'),
	url(regex=r'^(?P<owner_slug>[-\w]+)/protocolList/$', view=views.ProtocolListAPI.as_view(), name='protocol_list'),
)
