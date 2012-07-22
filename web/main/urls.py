from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    # Contents
    url(r'^', include("contents.urls")),

    # Blog
    # url(r'^admin/', include("blog.urls")),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

)
