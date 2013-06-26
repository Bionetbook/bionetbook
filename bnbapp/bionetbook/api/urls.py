from django.conf.urls.defaults import patterns, url, include

#from protocols import views
from api import views

urlpatterns = patterns("",
	# incomplete ajax:
	url(regex=r'^view/data_static/$', view=views.AjaxStaticView.as_view(), name='ajax_static_view'),
	
	url(regex=r'^json/data_dynamic/$', view='api.views.json_data_dynamic', name='json_data_dynamic'),
	url(regex=r'^view/ajax_dynamic/$', view=views.AjaxDynamicView.as_view(), name='ajax_dynamic_view'),
	
	url(regex=r'^json/ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view='api.views.get_layout_compare_json_v2', name='get_layout_compare_json_v2'),
	url(regex=r'^view/ajax/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view=views.AjaxView.as_view(), name='AjaxView'),
	
)








