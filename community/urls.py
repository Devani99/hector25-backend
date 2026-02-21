from django.urls import path
from .views import (
    PostListCreateView,
    PostDetailView,
    PostLikeToggleView,
    PostSaveToggleView,
    CommentListCreateView,
    CommentDeleteView,
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostLikeToggleView.as_view(), name='post-like-toggle'),
    path('posts/<int:pk>/save/', PostSaveToggleView.as_view(), name='post-save-toggle'),
    path('posts/<int:pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('posts/<int:pk>/comments/<int:cid>/', CommentDeleteView.as_view(), name='comment-delete'),
]
