from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="contents/index.html"), name="index"),
    url(r'^contact/$', TemplateView.as_view(template_name="contents/contact.html"), name="contact"),
)
