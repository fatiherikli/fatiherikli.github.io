from django.conf import settings
from django.contrib.sitemaps import Sitemap

from blog.models import Post


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9

    def items(self):
        return Post.published_objects.all()

    def lastmod(self, obj):
        return obj.date_modified

    def location(self, obj):
        return obj.get_absolute_url(prefix=None)

    def get_urls(self, page=1, site=None, protocol=None):

        class FakeSite:
            """
            A simple hack for sites framework.

            Sitemap framework is using sites framework for generating urls, and sites
            framework is not useful for this project.
            """
            domain = settings.BLOG_DOMAIN

        return super(BlogSitemap, self).get_urls(page, FakeSite(), protocol)
