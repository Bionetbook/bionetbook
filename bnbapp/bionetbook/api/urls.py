from django.conf.urls.defaults import patterns, url, include

#from protocols import views
from api import views

urlpatterns = patterns("",
	#url(regex=r'^v1/protocol/(?P<protocol_slug>[-\w]+)$', view='api.views.protocol_detail', name='api_detail'),
	url(regex=r'^jqtest/$', view=views.JQTestView.as_view(), name='api_jqtest'),		# FAILS
	url(regex=r'^protocoltest/(?P<protocol_a_slug>[-\w]+)/$', view=views.CompareLayersView.as_view(), name='api_protocoltest'),		# FAILS
	url(regex=r'^test/(?P<protocol_a_slug>[-\w]+)/$', view=views.TestView.as_view(), name='api_test'),				# WORKS
	url(regex=r'^json/(?P<protocol_slug>[-\w]+)/$', view='api.views.protocol_json', name='api_protocol_json'),
	url(regex=r'^json/layers/(?P<protocol_slug>[-\w]+)/$', view='api.views.protocol_layers_json', name='api_protocol_layers_json'),
	url(regex=r'^json/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view='api.views.protocol_compare_json', name='api_protocol_compare_json'),
	url(regex=r'^json/layers/(?P<protocol_a_slug>[-\w]+)/(?P<protocol_b_slug>[-\w]+)/$', view='api.views.protocol_diff_json', name='api_protocol_compare_layers_json'),
    # url(regex=r'^(?P<owner_slug>[-\w]+)/$', view=views.ProtocolListView.as_view(), name='organization_protocol_list'),
)








