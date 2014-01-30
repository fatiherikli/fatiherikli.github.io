from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.syndication.views import Feed
from django.http import HttpResponsePermanentRedirect, Http404
from django.utils.feedgenerator import Atom1Feed
from django.views.generic import ListView, RedirectView
from django.views.generic.detail import DetailView

from taggit.models import Tag, TaggedItem

from blog.models import Post


class BlogIndexView(ListView):
    template_name="blog/index.html"
    queryset = Post.published_objects.all()
    context_object_name = "posts"
    paginate_by = 100

    def get_queryset(self):
        queryset = super(BlogIndexView, self).get_queryset()
        self.cache_posts(queryset)
        return queryset

    def get_articles(self):
        """
        Returns articles if the user on first page.
        """
        try:
            page = int(self.request.GET.get("page"))
        except (ValueError, TypeError):
            page = 1

        if page > 1:
            return []

        queryset = self.queryset.filter(tags__name__in=["article"])
        self.cache_posts(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        return super(BlogIndexView, self).get_context_data(
            articles=self.get_articles(), **kwargs)

    def cache_posts(self, queryset):
        """
        `prefetch_related` doesn't work with generic relationships.
        django-taggit uses generic relationships for tagging.
        """
        content_type = ContentType.objects.get_for_model(queryset.model)
        tagged_items = TaggedItem.objects.\
        select_related("tag").filter(
            content_type=content_type,
            object_id__in=queryset.values_list("pk", flat=True))

        for post in queryset:
            post.cached_tags = [tagged_item.tag
                                for tagged_item in tagged_items
                                if tagged_item.object_id == post.pk]


class BlogSearchView(BlogIndexView):
    template_name= "blog/post_search.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = super(BlogSearchView, self).get_queryset()
        keyword = self.request.GET.get("keyword")

        if not keyword:
            return queryset.none()

        return queryset.filter(
            title__icontains = keyword,
            content__icontains = keyword,
        )

class BlogDetailView(DetailView):
    template_name= "blog/post_detail.html"
    model = Post
    context_object_name = "post"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.published_objects.all()

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


class LegacyPostRedirectView(RedirectView, DetailView):
    """
    Redirects old blog posts as permanently.
    """
    model = Post
    permanent = True
    slug_url_kwarg = 'legacy_post_id'
    slug_field = 'legacy_id'

    def get_redirect_url(self, **kwargs):
        return self.get_object().get_absolute_url()