import json
import requests
import html2text
from dateutil import parser

from django.conf import settings
from django.core.management.base import BaseCommand
from blog.models import Post


class Command(BaseCommand):
    """
    A command for importing posts from tumblr.
    """
    def handle(self, *args, **kwargs):
        self.import_posts()

    def import_posts(self, offset=0):
        request = json.loads(requests.get(
            "http://api.tumblr.com/v2/blog/%(blog_name)s"
            "/posts/text?api_key=%(api_key)s&offset=%(offset)s" % {
                "blog_name": settings.TUMBLR_BLOG_NAME,
                "api_key": settings.TUMBLR_API_KEY,
                "offset": offset
            }).content)

        for post in request["response"]["posts"]:
            self.add_post(post)

        if request["response"]["blog"]["posts"] > offset:
            self.import_posts(offset+20)


    def add_post(self, data):

        post_dict = self.clean_post(data)
        tags = post_dict.pop("tags", [])

        try:
            post = Post.objects.get(legacy_id=post_dict.get("legacy_id"))
        except Post.DoesNotExist:
            post = Post()

        for key, value in post_dict.items():
            setattr(post, key, value)

        post.save()

        post.tags.add(*tags)

        print post


    def clean_post(self, post):
        """
        Preparing data for Post model.
        """

        # html to markdown

        html_post = post["body"].replace("<br/>", "<br>") # html2text hack.

        text =  html2text.html2text(html_post)

        content_lines = text.splitlines()

        for i, line in enumerate(content_lines):
            if line.startswith("     "):
                del content_lines[i-1]

        return {
            "content": "\n".join(content_lines),
            "title": post["title"],
            "slug": post["slug"],
            "date_created": parser.parse(post["date"]),
            "tags": post["tags"],
            "legacy_url": post["post_url"],
            "legacy_id": post["post_url"].split("/")[4],
        }