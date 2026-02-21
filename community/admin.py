from django.contrib import admin
from .models import Post, Comment, Like, Save


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'likes_count', 'comments_count', 'created_at')
    search_fields = ('title', 'content', 'author__email')
    ordering = ('-created_at',)

    def likes_count(self, obj):
        return obj.likes.count()

    def comments_count(self, obj):
        return obj.comments.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content', 'author__email')
