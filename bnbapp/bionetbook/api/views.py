from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import django.utils.simplejson as json
from django.views.generic.detail import View, BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic import TemplateView
from django import http

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
        return {'name': "BOB", 'birthday':"now", 'cake':"none"}

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
    template_name = "api/test1.html"
    
    # def get(self, request):
    #     # <view logic>
    #             # self.object = self.get_object()
    #     context = {} #self.get_context_data(object=self.object)
    #     return self.render_to_response(context)

        # return render(request,  self.template_name)