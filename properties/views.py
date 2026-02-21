from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Property, Favorite
from .serializers import (
    PropertyListSerializer, PropertyDetailSerializer,
    PropertyWriteSerializer, FavoriteSerializer,
)
from .filters import PropertyFilter


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow write operations only to the property owner."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class PropertyListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/properties/         — list all properties (with filters)
    POST /api/properties/         — create a new property
    """
    queryset = Property.objects.select_related('owner').prefetch_related('images', 'amenities')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'location', 'description']
    ordering_fields = ['price', 'created_at', 'bedrooms']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PropertyWriteSerializer
        return PropertyListSerializer

    def create(self, request, *args, **kwargs):
        serializer = PropertyWriteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        property_obj = serializer.save()
        return Response(
            PropertyDetailSerializer(property_obj, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/properties/{id}/  — property detail
    PATCH  /api/properties/{id}/  — update (owner only)
    DELETE /api/properties/{id}/  — delete (owner only)
    """
    queryset = Property.objects.select_related('owner').prefetch_related('images', 'amenities')
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return PropertyWriteSerializer
        return PropertyDetailSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class FeaturedPropertiesView(generics.ListAPIView):
    """GET /api/properties/featured/ — featured and new launch properties."""
    serializer_class = PropertyListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        listing_type = self.request.query_params.get('listing_type', None)
        qs = Property.objects.filter(is_featured=True)
        if listing_type:
            qs = qs.filter(listing_type__iexact=listing_type)
        return qs


class FavoriteToggleView(APIView):
    """POST /api/properties/{id}/favorite/ — add or remove from favorites."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            property_obj = Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(
            user=request.user, property=property_obj
        )
        if not created:
            favorite.delete()
            return Response({'favorited': False}, status=status.HTTP_200_OK)
        return Response({'favorited': True}, status=status.HTTP_201_CREATED)


class UserFavoritesView(generics.ListAPIView):
    """GET /api/properties/favorites/ — list current user's favorited properties."""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('property')
