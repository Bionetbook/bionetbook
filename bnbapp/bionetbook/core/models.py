from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class SlugStampMixin(object):
    '''
    An Worflow is an ordered collection of a Protocols
    '''

    def save(self, *args, **kwargs):
        super(SlugStampMixin, self).save(*args, **kwargs) # Method may need to be changed to handle giving it a new name.
        
        new_slug = self.generate_slug()

        if not new_slug == self.slug: # Triggered when its a clone method
            self.slug = new_slug
            super(SlugStampMixin, self).save(*args, **kwargs) # Method may need to be changed to handle giving it a new name.


    def generate_slug(self):
        slug = slugify(self.name)

        if self.pk:
            return "%d-%s" % (self.pk, slug)
        else:
            return slug
