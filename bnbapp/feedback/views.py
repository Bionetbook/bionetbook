from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, CreateView
from braces.views import LoginRequiredMixin
from feedback.models import Feedback
from feedback.forms import FeedbackForm


class FeedbackView(CreateView):
    model = Feedback
    success_url = "/feedback/success/"
    form_class = FeedbackForm


class FeedbackSuccessView(TemplateView):
    template_name = 'feedback/feedback_success.html'

