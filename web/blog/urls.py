from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from blog.views import BlogIndexView, BlogDetailView, \
    LegacyPostRedirectionView, BlogPostsAtomFeed, BlogPostsRssFeed


urlpatterns = patterns('',

    # blog urls
    url(r'^$', BlogIndexView.as_view(), name="blog"),
    url(r'^post/(?P<slug>[-\w]+)/$',
        BlogDetailView.as_view(), name="blog_detail"),

    # rss & atom feed
    url(r'^feed/rss$', BlogPostsRssFeed(), name="blog_rss_feed"),
    url(r'^feed/atom', BlogPostsAtomFeed(), name="blog_atom_feed"),

    # legacy urls for old blog.fatiherikli.com
    url(r'^post/(?P<id>\d+)/(?P<slug>[-\w]+)$',
        LegacyPostRedirectionView.as_view(), name="blog_detail"),

    url(r'^rss', RedirectView.as_view(
        url="feed", permanent=True), name="blog_feed"),
)


