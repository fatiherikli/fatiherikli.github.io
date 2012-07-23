from django.views.generic.list import ListView

from blog.models import Post

class BlogIndexView(ListView):
    queryset = Post.published_objects.all()