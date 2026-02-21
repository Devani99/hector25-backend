from django.urls import path
from .views import (
    PropertyListCreateView,
    PropertyDetailView,
    FeaturedPropertiesView,
    FavoriteToggleView,
    UserFavoritesView,
)

urlpatterns = [
    path('', PropertyListCreateView.as_view(), name='property-list-create'),
    path('featured/', FeaturedPropertiesView.as_view(), name='property-featured'),
    path('favorites/', UserFavoritesView.as_view(), name='property-favorites'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('<int:pk>/favorite/', FavoriteToggleView.as_view(), name='property-favorite-toggle'),
]
