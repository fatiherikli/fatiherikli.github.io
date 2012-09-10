from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from blog.sitemaps import BlogSitemap

from blog.views import BlogIndexView, BlogDetailView, \
     BlogPostsAtomFeed, BlogPostsRssFeed, TagDetailView, BlogSearchView, LegacyPostRedirectView


urlpatterns = patterns('',

    # blog urls
    url(r'^$', BlogIndexView.as_view(), name="blog"),
    url(r'^search$', BlogSearchView.as_view(), name="blog_search"),
    url(r'^post/(?P<slug>[-\w]+)/$',
        BlogDetailView.as_view(), name="blog_detail"),
    url(r'^tag/(?P<slug>[-\w]+)/$',
        TagDetailView.as_view(), name="blog_tag_detail"),

    # rss & atom feed
    url(r'^feed/rss$', BlogPostsRssFeed(), name="blog_rss_feed"),
    url(r'^feed/atom', BlogPostsAtomFeed(), name="blog_atom_feed"),

    # sitemap
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': dict(
        blog=BlogSitemap()
    )}, name="blog_sitemap"),

    # legacy urls for oldest tumblr blog.
    url(r'^post/(?P<legacy_post_id>\d+)/(?P<slug>[-\w]+)$',
        LegacyPostRedirectView.as_view(), name="legacy_blog_detail"),
    url(r'^tagged/(?P<slug>[-\w]+)', RedirectView.as_view(
        url="/tag/%(slug)s", permanent=True), name="legacy_blog_tag_detail"),
    url(r'^rss', RedirectView.as_view(
        url="feed", permanent=True), name="legacy_blog_feed"),
)


