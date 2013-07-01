from django.template import Context, loader
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import django.utils.simplejson as json
from django.views.generic.detail import View, BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic import TemplateView
from django import http
from compare.models import ProtocolPlot, DictDiffer, Compare, CompareVerb, CompareChildren
from protocols.models import Protocol

def protocol_detail(request, protocol_slug):
    if request.method == 'GET':
        try:
            p = Protocol.objects.get(slug=protocol_slug)
            if p.data:
                return HttpResponse(json.dumps(p.data), mimetype="application/json")
            else:
                return HttpResponse(json.dumps({'error':'NoObjectData', 'description':'Requested protocol has no data.'}), mimetype="application/json")
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'error':'ObjectDoesNotExist', 'description':'Requested protocol could not be found.'}), mimetype="application/json")

def get_layout_json(request, protocol_a_slug):
    '''
    JSON call of a 2-protocol compare
    '''
    A = Protocol.objects.get(slug=protocol_a_slug)
    protocols = [A]
    G = Compare(protocols)
    G.get_layout_by_objectid()
    data = list(G.layout)
    
    return HttpResponse(json.dumps(data, indent = 4, separators=(',', ': ')), mimetype="application/json")     

def get_layout_compare_json(request, protocol_a_slug ,protocol_b_slug):
    '''
    JSON call of a 2-protocol compare
    '''
    A = Protocol.objects.get(slug=protocol_a_slug)
    B = Protocol.objects.get(slug=protocol_b_slug)
    protocols = [A,B]
    G = Compare(protocols)
    G.get_layout_by_objectid()
    data = list(G.layout)
    
    return HttpResponse(json.dumps(data, indent = 4, separators=(',', ': ')), mimetype="application/json")     

def json_data_dynamic(request):
    json_data = open("api/protocol_outline_double.json").read()
    data = json.loads(json_data)
    return HttpResponse(json.dumps(data, indent = 4, separators=(',', ': ')), mimetype="application/json")



# TESTING VIEWS:

# class AjaxSingleView(TemplateView):
#     template_name = "api/protocol_layout_1_ajax.html"           

# class AjaxStaticView(TemplateView):
#     template_name = "api/protocol_layout_3_static.html"

# class AjaxDynamicView(TemplateView):
#     template_name = "api/protocol_layout_3_dynamic.html"                

# class AjaxView(TemplateView):
#     template_name = "api/protocol_layout_3_ajax.html"       


#________________________________________________________________________________________________________________             


# def protocol_layers_json(request, protocol_slug):
#     '''
#     returns json with protocol data and child summaries.
#     '''
#     p = Protocol.objects.get(slug=protocol_slug)
#     out = []
    
#     for verb in p.get_actions():
#         print 'verb: ', verb
#         data_dict={}
#         data_dict['name'] = p.nodes[verb]['verb']
#         data_dict['objectid'] = p.nodes[verb]['objectid']
#         data_dict['URL'] = p.nodes[verb].action_update_url()
        
#         nodes = p.nodes[verb].children
#         if nodes:
#             data_dict['node_type'] = p.nodes[verb].childtype()
#             data_dict['node'] = [r.summary for r in p.nodes[verb].children]
#         else:
#             data_dict['node_type'] = p.nodes[verb].childtype()

#         out.append(data_dict)
#     return HttpResponse(json.dumps(out), mimetype="application/json") 


