import os

from django.core.management.base import BaseCommand

from blog.models import Post


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        path = args[0]

        for post in Post.objects.all():

            file_path = os.path.join(path, "%s.md" % post.slug)
            markdown_file = open(file_path, "w")
            markdown_file.write(post.content.raw.encode("utf-8"))
            markdown_file.close()