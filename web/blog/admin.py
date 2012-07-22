from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "is_published"]
    list_filter = ["is_published"]
    search_fields = ["title", "slug", "content"]


admin.site.register(Post, PostAdmin)