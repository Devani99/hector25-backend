from rest_framework import serializers
from .models import Post, Comment, Like, Save


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author_name', 'author_avatar', 'content', 'created_at')
        read_only_fields = ('id', 'author_name', 'author_avatar', 'created_at')

    def get_author_name(self, obj):
        return obj.author.name or obj.author.email

    def get_author_avatar(self, obj):
        request = self.context.get('request')
        if obj.author.avatar and request:
            return request.build_absolute_uri(obj.author.avatar.url)
        return None


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author_name', 'author_avatar', 'title', 'content',
            'likes_count', 'comments_count', 'is_liked', 'is_saved',
            'time_ago', 'created_at',
        )
        read_only_fields = (
            'id', 'author_name', 'author_avatar', 'likes_count',
            'comments_count', 'is_liked', 'is_saved', 'time_ago', 'created_at',
        )

    def get_author_name(self, obj):
        return obj.author.name or obj.author.email

    def get_author_avatar(self, obj):
        request = self.context.get('request')
        if obj.author.avatar and request:
            return request.build_absolute_uri(obj.author.avatar.url)
        return None

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saves.filter(user=request.user).exists()
        return False

    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        diff = now - obj.created_at
        if diff < timedelta(hours=1):
            return f"{int(diff.seconds / 60)}m"
        elif diff < timedelta(days=1):
            return f"{int(diff.seconds / 3600)}h"
        elif diff < timedelta(weeks=1):
            return f"{diff.days}d"
        else:
            return obj.created_at.strftime('%b %d')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
