from django.conf.urls import patterns, url

from blog.views import BlogIndexView

urlpatterns = patterns('',
    url(r'^$', BlogIndexView.as_view(template_name="blog/index.html"), name="blog"),
)
