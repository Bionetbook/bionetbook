from django.template import Context, loader
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson as json
from django.views.generic.detail import View, BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic import TemplateView
from django import http
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin

from compare.models import ProtocolPlot, DictDiffer, Compare, CompareVerb, CompareChildren
from protocols.models import Protocol
from schedule.models import Calendar
from protocols.utils import VERB_CHOICES, VERB_FORM_DICT

'''
API Documentation

The API should be formatted like so using CRUD methodology:

http://www.bionetbook.com/api/<version>/<resource>/(<id>/)

Up through version number should come from the main urls.py, everything after the version should be in the API app.

Example (GET):
http://www.bionetbook.com/api/v1/calendar/          - Returns a list of all calendars (names & ids) available to the USER:
http://www.bionetbook.com/api/v1/calendar/2/        - Returns all the events in the given calendar
http://www.bionetbook.com/api/v1/calendar/2/XRD234/ - Returns details for the given event
'''

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class EventAPI(JSONResponseMixin, LoginRequiredMixin, View):
    '''
    API Examples, CRUD

    POST: { 'meta':{...},
            'data':[ { 'id':'bnb-o1-e1-p1-AXBAGS-FFGGAX',
                       'tmpid':"...",
                       'status':'add'
                      },
                    ]
            }

    GET: {  'meta':{...},
            'data':[ {...},
                   ]
            }

    PUT: { 'meta':{...},
            'data':[ { 'id':'...',
                       'status':'update'
                      },
                    ]
            }

    DELETE: { 'meta':{...},
              'data':[ { 'id':'...',
                       'status':'delete'
                        },
                     ]
            }
    '''
    # NEEDS TO HANDLE GET, POST, UPDATE AND DELETE
    http_method_names = ['get', 'post', 'put', 'delete']

    def get(self, request, *args, **kwargs):
        curCal = get_object_or_404( Calendar, pk=1 )
        result = {'meta':{}, 'data':curCal }
        return self.render_to_response( result )

    def put(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        result = {'meta':{}, 'data':context }
        return self.render_to_response(result)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        result = {'meta':{}, 'data':context }
        return self.render_to_response(result)

    def delete(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        result = {'meta':{}, 'data':context }
        return self.render_to_response(result)


def calendar_json(request, pk):
    if request.method == 'GET':
        curCal = get_object_or_404(Calendar, pk=1)
        return HttpResponse( json.dumps( curCal.data ), mimetype="application/json" )



def protocol_detail(request, protocol_slug):
    if request.method == 'GET':
        try:
            p = Protocol.objects.get(slug=protocol_slug)
            if p.data:
                return HttpResponse(json.dumps(p.data), mimetype="application/json")
            else:
                return HttpResponse(json.dumps({'error':'NoObjectData', 'description':'Requested protocol has no data.'}), mimetype="application/json")
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'error':'ObjectDoes`NotExist', 'description':'Requested protocol could not be found.'}), mimetype="application/json")


def get_layout_json(request, protocol_a_slug):
    '''
    JSON call of a protocol diagram
    '''
    A = Protocol.objects.get(slug=protocol_a_slug)
    protocols = [A]
    G = Compare(protocols)
    G.get_layout_by_objectid()
    data = list(G.layout)
    verbatim = dict()
    verbatim['text'] = A.get_verbatim_text(numbers=True)
    data.append(verbatim)
    
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


def get_layout_clone_json(request, protocol_a_slug ,protocol_b_slug):
    '''
    JSON call of a 2-protocol compare
    '''
    A = Protocol.objects.get(slug=protocol_a_slug)
    B = Protocol.objects.get(slug=protocol_b_slug)
    protocols = [A,B]
    G = Compare(protocols)
    G.get_layout_by_objectid()
    [r.update(child_diff = "True") for r in G.layout]
    data = list(G.layout)

    return HttpResponse(json.dumps(data, indent = 4, separators=(',', ': ')), mimetype="application/json")     


def json_data_dynamic(request):
    json_data = open("api/protocol_outline_double.json").read()
    data = json.loads(json_data)
    return HttpResponse(json.dumps(data, indent = 4, separators=(',', ': ')), mimetype="application/json")


def get_verb_types_json(request):
    result = {'meta':{}, 'data':[{'name':x[0]} for x in VERB_CHOICES ] }
    return HttpResponse(json.dumps(result, indent = 4, separators=(',', ': ')), mimetype="application/json")


def get_verb_fields_json(request, slug):
    '''
    Returns a JSON result that lists all the form fields the verb type requires
    '''
    form = VERB_FORM_DICT[slug]

    # print dir(form)
    # 'add_initial_prefix', 'add_prefix', 'as_p', 'as_table', 'as_ul', 'base_fields', 'changed_data', 'clean', 'errors', 'full_clean', 'has_changed', 'has_component', 'has_machine', 'has_manual', 'has_thermocycler', 'hidden_fields', 'is_multipart', 'is_valid', 'layers', 'media', 'name', 'non_field_errors', 'slug', 'visible_fields'

    data = {'name':form.name,
            'has_components':form.has_component, 
            'has_machine':form.has_machine, 
            'has_thermocycler':form.has_thermocycler, 
            'visible_fields':[],
            'hidden_fields':[],
            }

    for key in form.base_fields:

        widget = field_to_json( form.base_fields[key] )
        widget['name'] = key

        data['visible_fields'].append( widget )

    result = {'meta':{}, 'data':data }

    # return HttpResponse( json.dumps( result ), mimetype="application/json")
    return HttpResponse(json.dumps(result, indent = 4, separators=(',', ': ')), mimetype="application/json")


def field_to_json(field):
    widget = {}

    # print dir(field)
    # 'bound_data', 'clean', 'creation_counter', 'default_error_messages', 'default_validators', 'error_messages', 'help_text', 'hidden_widget', 'initial', 'label', 'localize', 'max_value', 'min_value', 'prepare_value', 'required', 'run_validators', 'show_hidden_initial', 'to_python', 'validate', 'validators', 'widget', 'widget_attrs'

    if field.help_text:
        widget['help_text'] = field.help_text

    # print field.widget.input_type
    # 'attrs', 'build_attrs', 'context_instance', 'get_context', 'get_context_data', 'id_for_label', 'input_type', 'is_hidden', 'is_localized', 'is_required', 'media', 'needs_multipart_form', 'render', 'subwidgets', 'template_name', 'value_from_datadict'

    widget['input_type'] = field.widget.input_type

    # if field.widget.is_required:
    widget['is_required'] = field.widget.is_required

    # if field.widget.is_hidden:
    widget['is_hidden'] = field.widget.is_hidden

    return widget




# TESTING VIEWS:

# class AjaxSingleView(TemplateView):
#     template_name = "api/protocol_layout_1_ajax.html"           

class AjaxStaticView(TemplateView):
    template_name = "api/protocol_layout_3_static.html"

class AjaxDynamicView(TemplateView):
    template_name = "api/protocol_layout_3_dynamic.html"                

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


