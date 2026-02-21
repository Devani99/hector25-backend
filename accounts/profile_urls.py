from django.urls import path
from .views import ProfileView, AvatarUploadView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('avatar/', AvatarUploadView.as_view(), name='profile-avatar'),
]
