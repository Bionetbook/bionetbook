from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import django.utils.simplejson as json
from compare.models import ProtocolPlot, DictDiffer, Compare, CompareVerb, CompareChildren
from django import http
from django.views.generic.detail import View, BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic import TemplateView, View
from compare.utils import html_label_two_protocols, merge_table_pieces, add_step_label  
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin
from organization.models import Organization
from django.contrib import messages
from protocols.models import Protocol
import itertools
from protocols.utils import MANUAL_VERBS


class CompareSelectView(LoginRequiredMixin, TemplateView):
    model = Organization
    template_name = "compare/compare_select.html"
    slug_url_kwarg = "owner_slug"


    # GET THE PROTOCOLS THE USER CAN SEE
    def get_context_data(self, **kwargs):

        context = super(CompareSelectView, self).get_context_data(**kwargs)
        context['protocols'] = Protocol.objects.all()
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if slug:
            context['organization'] = Organization.objects.get(slug=slug)
        return context

    def post(self, request, *args, **kwargs):
        '''This is done to handle the two forms'''
        
        protocol_a = Protocol.objects.get(pk=int(request.POST['protocol_a']))
        protocol_b = Protocol.objects.get(pk=int(request.POST['protocol_b']))
        # NEED TO ADD CHECK TO MAKE SURE USER CAN SEE THESE PROTOCOLS

        url = reverse("compare_display_view", kwargs={'protocol_a_slug':protocol_a.slug, 'protocol_b_slug':protocol_b.slug})
        return HttpResponseRedirect(url)


class CompareDisplayView(CompareSelectView, TemplateView):          
    # template_name = "compare/protocol_layout_api_headers.html"           
    # template_name = "compare/protocol_layout_api_headers_temp_17.html"           
    template_name = "compare/protocol_layout_compare.html"           


    def get_context_data(self, **kwargs):
        context = super(CompareDisplayView, self).get_context_data(**kwargs)
        return context 
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        
        return self.render_to_response(context)    

class LayoutSingleView(TemplateView):
    # template_name = "compare/protocol_layout_api_1_headers.html"           

    # template_name = "compare/protocol_layout_api_1_headers_temp_17.html"           
    template_name = "compare/protocol_layout_single.html"           
    
    def get_context_data(self, **kwargs):

        context = super(LayoutSingleView, self).get_context_data(**kwargs)
        context['protocols'] = Protocol.objects.all()           # THIS NEEDS TO BE CHANGED SO THAT THE USER ONLY SEE WHAT THEY HVE PERMISSION TO CompareSelectView
        return context 
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['organization'] = context['protocol_a'].owner

        return self.render_to_response(context)    

class CloneLayoutSingleView(TemplateView):
    # template_name = "compare/protocol_layout_api_1_headers.html"           

    # template_name = "compare/protocol_layout_api_1_headers_temp_17.html"           
    # template_name = "compare/protocol_layout_compare.html"           
    
    def get_context_data(self, **kwargs):

        context = super(CloneLayoutSingleView, self).get_context_data(**kwargs)
        context['protocols'] = Protocol.objects.all()           # THIS NEEDS TO BE CHANGED SO THAT THE USER ONLY SEE WHAT THEY HVE PERMISSION TO CompareSelectView
        context['clone'] = True
        return context 
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        protocol = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['organization'] = protocol.owner
        slug_a = str(protocol.slug)
        protocol.clone()
        protocol.save()
        slug_b = str(protocol.slug)

        messages.add_message(self.request, messages.INFO, "Your protocol has been cloned.")
        
        url = reverse('clone_display_view', kwargs={'protocol_a_slug': slug_a, 'protocol_b_slug': slug_b})

        return http.HttpResponseRedirect(url)


# class 
class CloneDisplayView(TemplateView):          
    # template_name = "compare/protocol_layout_api_headers.html"           
    # template_name = "compare/protocol_layout_api_headers_temp_17.html"           
    template_name = "compare/protocol_layout_compare.html"           


    def get_context_data(self, **kwargs):
        context = super(CloneDisplayView, self).get_context_data(**kwargs)
        context['protocols'] = Protocol.objects.all()           # THIS NEEDS TO BE CHANGED SO THAT THE USER ONLY SEE WHAT THEY HVE PERMISSION TO CompareSelectView
        context['clone'] = True
        return context 
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        context['organization'] = context['protocol_a'].owner
        
        return self.render_to_response(context)    


class CompareDisplayView(CompareSelectView, TemplateView):          
    # template_name = "compare/protocol_layout_api_headers.html"           
    # template_name = "compare/protocol_layout_api_headers_temp_17.html"           
    template_name = "compare/protocol_layout_compare.html"           


    def get_context_data(self, **kwargs):
        context = super(CompareDisplayView, self).get_context_data(**kwargs)
        context['protocols'] = Protocol.objects.all()           # THIS NEEDS TO BE CHANGED SO THAT THE USER ONLY SEE WHAT THEY HVE PERMISSION TO CompareSelectView
        return context 
        
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['protocol_a'] = ProtocolPlot.objects.get(slug=kwargs['protocol_a_slug'])
        context['protocol_b'] = ProtocolPlot.objects.get(slug=kwargs['protocol_b_slug'])
        context['organization'] = context['protocol_a'].owner
        
        return self.render_to_response(context)    




