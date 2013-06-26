from django.conf.urls.defaults import patterns, url, include

#from protocols import views
from api import views

urlpatterns = patterns("",
	
	url(regex=r'^view/data_static/$', view=views.JsonStaticView.as_view(), name='JsonManulaView'),
	url(regex=r'^json/data_dynamic/$', view='api.views.json_data_dynamic', name='json_api_static'),
	url(regex=r'^view/ajax_dynamic/$', view=views.AjaxDynamicView.as_view(), name='AjaxDynamicView'),
	
	url(regex=r'^json/ajax/(?P<protocol_a_slug>[-\w]+)/$', view='api.views.get_layout_compare_json', name='json_api_static'),
	url(regex=r'^view/ajax/(?P<protocol_a_slug>[-\w]+)/$', view=views.AjaxView.as_view(), name='AjaxView'),
	
# depricated URLS:
	# url(regex=r'^jqtest/$', view=views.JQTestView.as_view(), name='api_jqtest'),		# FAILS
	url(regex=r'^json/all/$', view='api.views.json_dump_all', name='api_json_dump_all'),
	url(regex=r'^json/layers/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view='api.views.protocol_diff_json', name='api_protocol_compare_layers_json'),
	url(regex=r'^json/(?P<protocol_slug>[-\w]+)/$', view='api.views.protocol_json', name='api_protocol_json'),
	
)








