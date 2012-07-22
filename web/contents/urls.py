from django.conf.urls import patterns
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
    (r'^$', TemplateView.as_view(template_name="contents/index.html")),
    (r'^contact/$', TemplateView.as_view(template_name="contents/contact.html")),
)
