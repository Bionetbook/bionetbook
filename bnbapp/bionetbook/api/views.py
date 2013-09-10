from django.template import Context, loader
from django.http import HttpResponse, Http404, QueryDict
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson as json
from django.views.generic.detail import View, BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin
from django import http
from django.shortcuts import get_object_or_404
from django.conf import settings
import ast

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
<<<<<<< HEAD

(PUT)
=======
>>>>>>> master
http://www.bionetbook.com/api/v1/calendar/2/bnb-o1-e1-p1-AXBAGS-FFGGAX/ - Returns details for the given event
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
        if not settings.DEBUG:                  # USE THE MORE EFFICIENT WAY IN PROTDUCTION
            return json.dumps(context)
        else:
            return json.dumps(context, indent = 4, separators=(',', ': '))

    def put_request_scrub(self, request):
        if hasattr(request, '_post'):
            del request._post
            del request._files
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST
        return request

    def context_package(self, **kwargs):
        result = {}

        for key in ['data', 'meta', 'error']:
            if key in kwargs:
                result[key] = kwargs[key]

        return result


##############
# CALENDAR API
##############

class SingleEventAPI(JSONResponseMixin, LoginRequiredMixin, View):
    '''
    SingleEventAPI returns a single event from a calendar

    GET:
    {   'id':"bnb-o1-e1-p1-AXBAGS-FFGGAX":,
        'start':1376957033,
        'duration':300,
        'title':"First Action",
        'protocol':'dna-jalkf',
        'experiment':'experiment 1',
        'notes':"",
        'verb':"mix"
    }

    PUT:
    On success:
    {
        'id':"bnb-o1-e1-p1-AXBAGS-FFGGAX",
        'start':12321311231,
        'notes':"",
        'status':"updated"
    }
    On failure: 
    404
    '''

    http_method_names = ['get', 'post', 'put']

    def get(self, request, *args, **kwargs):
        eventID = self.kwargs['event_id']
        cal = get_object_or_404(Calendar, pk=self.kwargs['pk'])
        for event in cal.data['events']:
            if eventID in event.values():
                return self.render_to_response ( event )
        raise Http404

    def put(self, request, *args, **kwargs):
        request = self.put_request_scrub(request)
        event = request.PUT
        eventID = self.kwargs['event_id']
        cal = get_object_or_404(Calendar, pk=self.kwargs['pk'])
        if eventID == event['id']:
            for e in cal.data['events']:
                if eventID in e.values():
                    e['start'] = event['start']
                    e['notes'] = event['notes']
                    cal.save()
                    return self.render_to_response ( { 'id':e['id'], 'start':e['start'], 'notes':e['notes'], 'status':'updated'} )
        raise Http404


class ListCalendarAPI(JSONResponseMixin, LoginRequiredMixin, View):
    
    '''
    ListCalendarAPI returns a list of calendars belonging to the user with their pk

    {
        'calendars': ['Andrew's Calendar-1', 'Public Calendar-2', 'Misc Calendar-3']
    }
    '''

    http_method_names = ['get', 'post', 'put']

    def get(self, request, *args, **kwargs):
        usersCalendars = []
        if self.request.user.is_authenticated():
            for cal in self.request.user.calendar_set.all():
                usersCalendars.append('%s-%s' % (cal.name, cal.pk))
        return self.render_to_response ( {'calendars':usersCalendars} )


class SingleCalendarAPI(JSONResponseMixin, LoginRequiredMixin, View):
    '''
    API Examples, CRUD

    GET: {  'meta':{...},
            'events':[ {...},
                   ]
            }
    PUT: Input: {
            'events': [{ },{ }]
        }
        Output: 200
        }
    '''
    # NEEDS TO HANDLE GET, POST, UPDATE AND DELETE
    http_method_names = ['get', 'put', 'delete']

    def get(self, request, *args, **kwargs):
        curCal = get_object_or_404( Calendar, pk=self.kwargs['pk'])
        return self.render_to_response( curCal.data )

    # Return 200 always unless wrong pk for calendar
    def put(self,request, *args, **kwargs):
        request = self.put_request_scrub(request)
        #print request.PUT.getlist('events')[0] + " " + request.PUT.getlist('events')[1]
        eventList = dict(request.PUT.iterlists())['events']
        cal = get_object_or_404(Calendar, pk=self.kwargs['pk'])
        for event in eventList:   # [ {event}, { } ]
            event = ast.literal_eval(event)
            for eCal in cal.events():
                if event['id'] in eCal.values():
                    eCal['start'] = event['start']
                    eCal['notes'] = event['notes']
                    continue
        cal.save()    
        return HttpResponse()        


##############
# PROTOCOL API
##############

class ProtocolAPI(JSONResponseMixin, LoginRequiredMixin, View):     # NEED A PREMISSION CHECK HERE
    '''
    Returns the Protocol in JSON form.  Will provide update and edit mehtods.

    Can be used with either a Primary Key or Slug.

    API Examples, CRUD

    GET: {  'meta':{...},
            'data':{...<PROTOCOL>...},
            'error':
            }
    '''

    # NEEDS TO HANDLE GET, POST, UPDATE AND DELETE
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_protocol(self):
        '''Unified method to get a protocol via ID or Slug'''
        if 'protocol_slug' in self.kwargs:
            result = get_object_or_404( Protocol, slug=self.kwargs['protocol_slug'] )
        else:
            result = get_object_or_404( Protocol, id=self.kwargs['protocol_id'] )

        #CHECK TO SEE IF THE USER HAS PERMISSIONS TO VIEW THIS PROTOCOL AND 404 IF NOT

        return result

    def get(self, request, *args, **kwargs):
        '''Read only method for getting a protocol in JSON format'''
        protocol = self.get_protocol()

        if protocol.data:
            return self.render_to_response( self.context_package( data=protocol.as_dict() ) )
        else:
            return self.render_to_response( self.context_package( error={'type':'NoObjectData', 'description':'Requested protocol has no data.'} ) )

    def put(self, request, *args, **kwargs):
        request = self.put_request_scrub(request)
        print "PUT REQUEST:"
        print request.PUT
        # event = request.PUT
        # eventID = self.kwargs['event_id']
        # cal = get_object_or_404(Calendar, pk=self.kwargs['pk'])
        # if eventID == event['id']:
        #     for e in cal.data['events']:
        #         if eventID in e.values():
        #             e['start'] = event['start']
        #             e['notes'] = event['notes']
        #             cal.save()
        #             return self.render_to_response ( { 'id':e['id'], 'start':e['start'], 'notes':e['notes'], 'status':'updated'} )
        # raise Http404


# class ProtocolDataAPI(JSONResponseMixin, LoginRequiredMixin, View):
#     '''
#     '''
#     def get(self, request, *args, **kwargs):
#         p = get_object_or_404( Protocol, slug=kwargs['protocol_slug'] )
#         if p.data:
#             return self.render_to_response(p.data)
#         else:
#             return self.render_to_response({'error':'NoObjectData', 'description':'Requested protocol has no data.'})

# REPLACE WITH CLASS BASED VIEW ABOVE
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


class ProtocolLayoutAPI(JSONResponseMixin, LoginRequiredMixin, View):
    '''
    JSON call of a protocol diagram handling 1 and 2 protocols
    '''
    def get(self, request, *args, **kwargs):
        single_protocol = True
        protocol_a = get_object_or_404( Protocol, slug=kwargs['protocol_a_slug'] )
        protocols = [protocol_a]

        if 'protocol_b_slug' in kwargs:
            protocol_b = get_object_or_404( Protocol, slug=kwargs['protocol_b_slug'] )
            protocols.append( protocol_b )
            single_protocol = False

        comp = Compare( protocols )
        comp.get_layout_by_objectid()
        data = list(comp.layout)

        if single_protocol:
            data.append( { 'text':protocol_a.get_verbatim_text(numbers=True) } )

        return self.render_to_response(data)


# REPLACE WITH CLASS BASED VIEWS ABOVE
# def get_layout_json(request, protocol_a_slug):
#     '''
#     JSON call of a protocol diagram
#     '''
#     A = Protocol.objects.get(slug=protocol_a_slug)
#     protocols = [A]
#     G = Compare(protocols)
#     G.get_layout_by_objectid()
#     data = list(G.layout)
#     verbatim = dict()
#     verbatim['text'] = A.get_verbatim_text(numbers=True)
#     data.append(verbatim)
    
#     return HttpResponse(json.dumps(data, indent = 4, separators=(',', ': ')), mimetype="application/json")     

# REPLACE WITH CLASS BASED VIEWS ABOVE
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





class VerbFieldAPI(JSONResponseMixin, LoginRequiredMixin, View):
    '''
    JSON call of a protocol diagram handling 1 and 2 protocols
    '''
    def get(self, request, *args, **kwargs):
        
        form = VERB_FORM_DICT[ kwargs['slug'] ]

        data = {'name':form.name,
                'has_components':form.has_component, 
                'has_machine':form.has_machine, 
                'has_thermocycler':form.has_thermocycler, 
                'visible_fields':[],
                'hidden_fields':[],
                }

        for key in form.base_fields:
            form_field = form.base_fields[key]
            widget = self.field_to_json( key, form_field )

            # NEED TO ADD LABEL FIELD
            if form_field.widget.is_hidden:
                data['hidden_fields'].append( widget )
            else:
                data['visible_fields'].append( widget )

        return self.render_to_response(data)

    def field_to_json(self, key, field):
        widget = {}

        # print dir(field)
        # 'bound_data', 'clean', 'creation_counter', 'default_error_messages', 'default_validators', 'error_messages', 'help_text', 'hidden_widget', 'initial', 'label', 'localize', 'max_value', 'min_value', 'prepare_value', 'required', 'run_validators', 'show_hidden_initial', 'to_python', 'validate', 'validators', 'widget', 'widget_attrs'

        if field.help_text:
            widget['help_text'] = field.help_text

        # print field.widget.input_type
        # 'attrs', 'build_attrs', 'context_instance', 'get_context', 'get_context_data', 'id_for_label', 'input_type', 'is_hidden', 'is_localized', 'is_required', 'media', 'needs_multipart_form', 'render', 'subwidgets', 'template_name', 'value_from_datadict'

        widget['input_type'] = field.widget.input_type
        widget['name'] = key

        if field.label:
            widget['label'] = field.label
        else:
            widget['label'] = " ".join([ x.capitalize() for x in key.split("_")] )
        
        widget['is_required'] = field.widget.is_required

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


