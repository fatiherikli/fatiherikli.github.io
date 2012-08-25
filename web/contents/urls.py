from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from contents.views import ContactView


urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(
        template_name="contents/index.html"
    ), name="index"),

    url(r'^contact/$', ContactView.as_view(
        template_name="contents/contact.html"
    ), name="contact"),

    url(r'^contact/success/$', TemplateView.as_view(
        template_name="contents/contact_success.html"
    ), name="contact_success"),

    # static files
    url(r'^humans.txt$', TemplateView.as_view(
        template_name="humans.txt"
    ), name="humans"),

    url(r'^robots.txt$', TemplateView.as_view(
        template_name="robots.txt"
    ), name="robots"),
    
)
