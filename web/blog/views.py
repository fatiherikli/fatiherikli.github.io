from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blog.models import Post


class BlogIndexView(ListView):
    template_name="blog/index.html"
    queryset = Post.published_objects.all()
    context_object_name = "posts"
    paginate_by = 20


class BlogDetailView(DetailView):
    template_name="blog/detail.html"
    queryset = Post.published_objects.all()
    context_object_name = "post"
