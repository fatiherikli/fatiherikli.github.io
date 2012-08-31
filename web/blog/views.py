from django.conf import settings
from django.contrib.syndication.views import Feed
from django.http import HttpResponsePermanentRedirect
from django.utils.feedgenerator import Atom1Feed
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from taggit.models import Tag
from blog.forms import SearchForm

from blog.models import Post


class BlogIndexView(ListView):
    template_name="blog/index.html"
    queryset = Post.published_objects.all()
    context_object_name = "posts"
    paginate_by = 10

class BlogSearchView(BlogIndexView):
    template_name= "blog/post_search.html"
    paginate_by = 20

    def get_queryset(self):
        keyword = self.request.GET.get("keyword")
        queryset = super(BlogSearchView, self).get_queryset()

        if not keyword:
            return queryset.none()

        return queryset.filter(
            title__icontains = keyword,
            content__icontains = keyword,
        )

class BlogDetailView(DetailView):
    template_name= "blog/post_detail.html"
    queryset = Post.published_objects.all()
    context_object_name = "post"

class TagDetailView(DetailView):
    queryset = Tag.objects.all()
    template_name= "blog/tag_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data()
        posts = Post.objects.filter(tags__in=[self.object])
        context.update({
            "posts": posts
        })
        return context

class BlogPostsRssFeed(Feed):
    title = settings.BLOG_FEED_TITLE
    link = settings.BLOG_URL
    description = settings.BLOG_FEED_DESCRIPTION

    def items(self):
        return Post.objects.all()[:20]

    def item_description(self, post):
        return post.content

    def item_pubdate(self, post):
        return post.date_created

    def item_categories(self, post):
        return [tag.name for tag in post.tags.all()]


class BlogPostsAtomFeed(BlogPostsRssFeed):
    feed_type = Atom1Feed
    subtitle = settings.BLOG_FEED_DESCRIPTION


class LegacyPostRedirectionView(DetailView):
    """
    Redirects old blog posts as permanently.
    """
    model = Post

    def render_to_response(self, context, **response_kwargs):
        return HttpResponsePermanentRedirect(
            context.get("object").get_absolute_url())


