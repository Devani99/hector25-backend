from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count

from .models import Post, Comment, Like, Save
from .serializers import PostSerializer, CommentSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow write operations only to the post/comment author."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/community/posts/         — list posts
    POST /api/community/posts/         — create post (authenticated)

    Query params:
      ?tab=trending   — order by likes count desc
      ?tab=for_you    — default chronological
    """
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        tab = self.request.query_params.get('tab', 'for_you')
        qs = Post.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
        )
        if tab == 'trending':
            qs = qs.order_by('-likes_count', '-created_at')
        else:
            qs = qs.order_by('-created_at')
        return qs


class PostDetailView(generics.RetrieveDestroyAPIView):
    """
    GET    /api/community/posts/{id}/  — post detail
    DELETE /api/community/posts/{id}/  — delete (author only)
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Post.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
        )

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]


class PostLikeToggleView(APIView):
    """POST /api/community/posts/{id}/like/ — toggle like on a post."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({'liked': False, 'likes_count': post.likes.count()})
        return Response({'liked': True, 'likes_count': post.likes.count()}, status=status.HTTP_201_CREATED)


class PostSaveToggleView(APIView):
    """POST /api/community/posts/{id}/save/ — toggle save (bookmark) on a post."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        save, created = Save.objects.get_or_create(post=post, user=request.user)
        if not created:
            save.delete()
            return Response({'saved': False})
        return Response({'saved': True}, status=status.HTTP_201_CREATED)


class CommentListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/community/posts/{id}/comments/  — list comments
    POST /api/community/posts/{id}/comments/  — add comment (authenticated)
    """
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['pk']).select_related('author')

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(pk=self.kwargs['pk'])
        except Post.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound('Post not found.')
        serializer.save(author=self.request.user, post=post)


class CommentDeleteView(generics.DestroyAPIView):
    """DELETE /api/community/posts/{pk}/comments/{cid}/ — delete comment (author only)."""
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['pk'])

    def get_object(self):
        from django.shortcuts import get_object_or_404
        return get_object_or_404(Comment, pk=self.kwargs['cid'], post_id=self.kwargs['pk'])
