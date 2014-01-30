from blog.forms import SearchForm
from blog.models import Post

def latest_posts(request):
    return {
        "latest_posts": Post.published_objects.all()[:10]
    }

def search(request):
    keyword = request.GET.get("keyword")
    search_data = None if keyword is None else request.GET
    return {
        "search_form": SearchForm(search_data),
        "keyword": keyword
    }