from django.conf.urls.defaults import patterns, url, include

#from protocols import views
from api import views1

urlpatterns = patterns("",
	#url(regex=r'^v1/protocol/(?P<protocol_slug>[-\w]+)$', view='api.views.protocol_detail', name='api_detail'),
	url(regex=r'^jqtest/$', view=views1.JQTestView.as_view(), name='api_jqtest'),		# FAILS
	url(regex=r'^protocoltest/(?P<protocol_a_slug>[-\w]+)/$', view=views1.CompareLayersView.as_view(), name='api_protocoltest'),		# FAILS
	url(regex=r'^test/$', view=views1.TestView.as_view(), name='api_test'),				# WORKS
    # url(regex=r'^(?P<owner_slug>[-\w]+)/$', view=views.ProtocolListView.as_view(), name='organization_protocol_list'),
)


