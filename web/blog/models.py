from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from markitup.fields import MarkupField
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """
    Returns published blog posts.
    """
    def get_query_set(self):
        return super(PublishedManager, self)\
        .get_query_set().filter(is_published=True)


class Post(models.Model):
    """
    Holds blog post data.
    """
    title = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True)
    content = MarkupField(_("Content"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    is_published = models.BooleanField(_("Published"), default=True)
    cover_image = models.ImageField(upload_to="covers/", null=True, blank=True)

    # legacy fields
    legacy_url = models.URLField(_("Legacy URL"), blank=True, null=True, editable=False)
    legacy_id = models.IntegerField(_("Legacy Post ID"), blank=True, null=True)

    objects = models.Manager()
    published_objects = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ("-date_created", )

    def __unicode__(self):
        return smart_unicode(self.title)

    def get_absolute_url(self, prefix=settings.BLOG_URL):
        return reverse("blog_detail", args=[self.slug, ],
            urlconf="blog.urls", prefix=prefix)

    def get_tags(self):
        if hasattr(self, "cached_tags"):
            return self.cached_tags
        return self.tags.all()