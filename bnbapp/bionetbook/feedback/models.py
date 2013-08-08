from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel

FEEDBACK_CHOICES = (('feedback','Feedback'), ('business','Business Inquery'), ('bug','Bug Report'), )
RESOLUTION_CHOICES = (('open','Open'),('resolved','Resolved') )

# Create your models here.
from django.utils.translation import ugettext_lazy as _

class Feedback(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=60)
    email = models.CharField(_("Email"), max_length=50)
    classification = models.CharField(_("Classification"), default="feedback", choices=FEEDBACK_CHOICES, max_length=30)
    description = models.TextField(_("Description") )
    resolved_by = models.ForeignKey(User, blank=True, null=True)
    resolution = models.CharField(_("Resolution"), default="open", choices=RESOLUTION_CHOICES, max_length=30)
    notes = models.TextField(_("Description") )


    #widget=forms.Textarea(attrs={'rows': 3, 'class':'textarea span12'})

    class Meta:
        verbose_name_plural = "Feedback"
