from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from actions.models import Action


class Very(TimeStampedModel):

    step = models.OneToOneField(Action)
    name = models.CharField(_("Name"), max_length=255)
    # attributes = TODO

    def __unicode__(self):
        return self.name
