"""
URL configuration for hector25_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

admin.site.site_header = "Hector25 Admin"
admin.site.site_title = "Hector25 Admin Portal"
admin.site.index_title = "Welcome to Hector25 Admin"


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    Hector25 REST API — root endpoint listing all available resources.
    """
    return Response({
        'info': 'Hector25 Real Estate Backend API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'register':      reverse('auth-register',      request=request),
                'login':         reverse('auth-login',         request=request),
                'logout':        request.build_absolute_uri('/api/auth/logout/'),
                'token_refresh': request.build_absolute_uri('/api/auth/token/refresh/'),
                'me':            reverse('auth-me',            request=request),
            },
            'profile': {
                'view_update':   reverse('profile',            request=request),
                'avatar_upload': reverse('profile-avatar',     request=request),
            },
            'properties': {
                'list_create':   reverse('property-list-create', request=request),
                'featured':      reverse('property-featured',    request=request),
                'my_favorites':  reverse('property-favorites',   request=request),
                'detail':        request.build_absolute_uri('/api/properties/{id}/'),
                'toggle_fav':    request.build_absolute_uri('/api/properties/{id}/favorite/'),
            },
            'community': {
                'posts':         reverse('post-list-create',   request=request),
                'post_detail':   request.build_absolute_uri('/api/community/posts/{id}/'),
                'like':          request.build_absolute_uri('/api/community/posts/{id}/like/'),
                'save':          request.build_absolute_uri('/api/community/posts/{id}/save/'),
                'comments':      request.build_absolute_uri('/api/community/posts/{id}/comments/'),
            },
            'notifications': {
                'list':          reverse('notification-list',  request=request),
                'mark_all_read': reverse('notification-read-all', request=request),
                'mark_read':     request.build_absolute_uri('/api/notifications/{id}/read/'),
            },
            'admin_panel':       request.build_absolute_uri('/admin/'),
        },
        'filter_examples': {
            'search_apartments_rent': request.build_absolute_uri(
                '/api/properties/?type=Apartment&listing_type=rent&price_max=1000000'
            ),
            'search_villas_buy': request.build_absolute_uri(
                '/api/properties/?type=Villa&listing_type=buy&bedrooms=4'
            ),
            'trending_posts': request.build_absolute_uri(
                '/api/community/posts/?tab=trending'
            ),
            'featured_new_launch': request.build_absolute_uri(
                '/api/properties/featured/?listing_type=new_launch'
            ),
        }
    })


urlpatterns = [
    path('',         api_root, name='api-root'),
    path('api/',     api_root, name='api-root-prefix'),
    path('admin/',   admin.site.urls),
    path('api/auth/',          include('accounts.urls')),
    path('api/profile/',       include('accounts.profile_urls')),
    path('api/properties/',    include('properties.urls')),
    path('api/community/',     include('community.urls')),
    path('api/notifications/', include('notifications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
