from django.conf import settings
from django.core.urlresolvers import reverse

def urls(request):
    return {
        "urls": {

            # sub-domains
            "index": settings.MAIN_URL,
            "blog": settings.BLOG_URL,
            "sitemap": reverse("blog_sitemap",
                urlconf="blog.urls", prefix=settings.BLOG_URL),

            # internal links
            "blog_search": reverse("blog_search",
                urlconf="blog.urls", prefix=settings.BLOG_URL),
            "blog_rss_feed": reverse("blog_rss_feed",
                urlconf="blog.urls", prefix=settings.BLOG_URL),
            "blog_atom_feed": reverse("blog_atom_feed",
                urlconf="blog.urls", prefix=settings.BLOG_URL),
            "contact": reverse("contact",
                urlconf="main.urls", prefix=settings.MAIN_URL),


            # static contents
            "humans": reverse("humans", urlconf="main.urls"),
            "robots": reverse("robots", urlconf="main.urls"),


            # social media
            "twitter": "http://twitter.com/%s" % settings.TWITTER_USERNAME,
            "github": "http://github.com/%s" % settings.GITHUB_USERNAME,
            "google": "https://plus.google.com/%s" % settings.GOOGLE_ID,
        }
    }