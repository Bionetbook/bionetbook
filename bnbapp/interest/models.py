from django.db import models
from django_extensions.db.models import TimeStampedModel

class Interest(TimeStampedModel):

    email = models.EmailField(max_length=100)

    def __unicode__(self):
        return self.email

