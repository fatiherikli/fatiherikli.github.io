from blog.models import Post

def latest_posts(request):
    return {
        "latest_posts": Post.objects.all()[:10]
    }