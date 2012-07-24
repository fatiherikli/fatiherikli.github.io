from django.conf.urls import patterns, url

from blog.views import BlogIndexView, BlogDetailView

urlpatterns = patterns('',
    url(r'^$', BlogIndexView.as_view(), name="blog"),
    url(r'^post/(?P<slug>[-\w]+)/$', BlogDetailView.as_view(), name="blog_detail"),
)
