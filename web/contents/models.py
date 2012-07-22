from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from markitup.fields import MarkupField


class ContentBlock(models.Model):
    """
    Holds content block data.
    """
    name = models.SlugField(_("Name"), max_length=255)
    content = MarkupField()

    def __unicode__(self):
        return smart_unicode(self.name)