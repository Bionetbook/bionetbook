from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import django.utils.simplejson as json
from django.views.generic.detail import View, BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic import TemplateView
from django import http
from compare.models import ProtocolPlot, DictDiffer
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


def json_dump(request, protocol_slug):
    '''
    Very simple JSON Call example.
    '''
    p = Protocol.objects.get(slug=protocol_slug)
    data_dict = {'name':p.name, 'pk':p.pk}
    return HttpResponse(json.dumps(data_dict), mimetype="application/json")




def json_dump_all(request):
    '''
    Very simple JSON Call example.
    '''
    p = Protocol.objects.filter(published=True, public=True)
    result = [{'name':x.name, 'pk':x.pk} for x in p]
    return HttpResponse(json.dumps(result), mimetype="application/json")


class JSONResponseMixin(object):
    # def render_to_response(self, context):
    #     "Returns a JSON response containing 'context' as payload"
    #     return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an HttpResponse object."
        return http.HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


# class JQTestView(TemplateView):
#     template_name = "api/test.html"

class JQTestView(JSONResponseMixin, TemplateView):

    def get_context(self):
        context = super(JQTestView, self).get_context_data()
        protocol_a = Protocol.objects.get(pk=3)
        JSONdata = [protocol_a.nodes[r] for r in protocol_a.get_actions]
        num_verbs = len(protocol_a.get_actions)
        y_height = 30
        y_spacer = 15
        y_max = num_verbs * y_height + (num_verbs-1) * y_spacer
        spacing = range(0,y_max, y_height + y_spacer)
        y_position = dict((x,y) for x,y in zip(protocol_a.get_actions,spacing))

        # add URLS and y position to action 
        for t in JSONdata:
            t[u'url']= protocol_a.nodes[t['objectid']].action_update_url()
            t[u'position'] = y_position[t['objectid']]
       
        # context['data'] = json.dumps(JSONdata)    
        return JSONdata
        # return [{'name': "BOB", 'birthday':"now", 'cake':"none"}]

    def render_to_response(self, context, **httpresponse_kwargs):
        context = self.get_context()

        #if self.request.is_ajax():
        return self.get_json_response(self.convert_context_to_json(context))
        #return JSONResponseMixin.render_to_response(self, context)

        #return self.render_to_response(self, {'one':"two"})

        # if self.request.is_ajax():
        #     #obj = context['object'].as_dict()
        #     obj = {'name': "BOB", 'birthday':"yesterday"}
        #     HttpResponse(obj, content_type='application/json', **httpresponse_kwargs)
        #     #return self.render_to_response(self, obj)
        # else:
        #     #return SingleObjectTemplateResponseMixin.render_to_response(self, context)
        #     return self.render_to_response(self, {'one':"two"})



class TestView(TemplateView):
    template_name = "api/protocol_basic.html"
    
    # def get(self, request):
    #     # <view logic>
    #             # self.object = self.get_object()
    #     context = {} #self.get_context_data(object=self.object)
    #     return self.render_to_response(context)

        # return render(request,  self.template_name)


class CompareBaseView(JSONResponseMixin, TemplateView):
    # template_name = "compare/compare_default.html"

    def get(self, request, *args, **kwargs):
        '''Gets the context data'''
        arguments={}
        context = self.get_context_data()
        nodes = ['thermo', 'machine', 'component', 'steps', 'manual']

        protocol_a = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        # context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        display = 'single'
        arguments={'protocol_a_slug':context['protocol_a'].slug}              
        
        if 'protocol_b_slug' in kwargs and kwargs['protocol_b_slug'] != 'layers':
            
            context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
            display = 'double'
            arguments={'protocol_a_slug':context['protocol_a'].slug, 'protocol_b_slug':context['protocol_b'].slug}

        # assemble JSON object for JS D3:
        JSONdata = [protocol_a.nodes[r] for r in protocol_a.get_actions]
        
        # set position variables:
        num_verbs = len(protocol_a.get_actions)
        y_height = 30
        y_spacer = 15
        y_max = num_verbs * y_height + (num_verbs-1) * y_spacer
        spacing = range(0,y_max, y_height + y_spacer)
        y_position = dict((x,y) for x,y in zip(protocol_a.get_actions,spacing))

        # add URLS and y position to action 
        for t in JSONdata:
            t[u'url']= protocol_a.nodes[t['objectid']].action_update_url()
            t[u'position'] = y_position[t['objectid']]
            

        context['data'] = json.dumps(JSONdata)
        context['steps'] = context['protocol_a'].steps 
        context['position_data'] = json.dumps([y_height, y_spacer, y_max ])               
        
        return HttpResponse(context) #get_json_response(self.convert_context_to_json(JSONdata))



class CompareLayersView(CompareBaseView, TemplateView):
    template_name = "compare/protocol_basic.html"        


