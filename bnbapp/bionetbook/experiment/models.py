from django.db import models

# Create your models here.

#   Commenting out for now until this is formally ready to be added and all the fields are worked out
#
# class Experiment(TimeStampedModel):
#     experimentist = models.ForeignKey(User, blank=True, null=True)
#     workflow = models.ForeignKey(Workflow)
#     owner = models.ForeignKey(Organization)
#     name = models.CharField(_("Name"), max_length=255, unique=True)
#     slug = models.SlugField(_("Slug"), blank=True, null=True, max_length=255)
#     duration = models.IntegerField(_("Duration in seconds"), blank=True, null=True)
#     description = models.TextField(_("Description"), blank=True, null=True)
#     experiment_data = JSONField(blank=True, null=True)

