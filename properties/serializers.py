from rest_framework import serializers
from .models import Property, PropertyImage, Amenity, Favorite


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ('id', 'name', 'icon')


class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ('id', 'image_url', 'order')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class PropertyListSerializer(serializers.ModelSerializer):
    """Compact serializer for list views."""
    primary_image = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            'id', 'title', 'location', 'price', 'type', 'listing_type',
            'bedrooms', 'bathrooms', 'area_sqft', 'is_featured',
            'primary_image', 'is_favorited', 'created_at',
        )

    def get_primary_image(self, obj):
        request = self.context.get('request')
        img = obj.images.first()
        if img and request:
            return request.build_absolute_uri(img.image.url)
        return None

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(user=request.user).exists()
        return False


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail view."""
    images = PropertyImageSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    owner_name = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            'id', 'title', 'description', 'location', 'price', 'type',
            'listing_type', 'bedrooms', 'bathrooms', 'area_sqft', 'is_featured',
            'images', 'amenities', 'owner_name', 'is_favorited',
            'created_at', 'updated_at',
        )

    def get_owner_name(self, obj):
        return obj.owner.name or obj.owner.email

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(user=request.user).exists()
        return False


class PropertyWriteSerializer(serializers.ModelSerializer):
    """Used for creating/updating properties."""
    class Meta:
        model = Property
        fields = (
            'title', 'description', 'location', 'price', 'type',
            'listing_type', 'bedrooms', 'bathrooms', 'area_sqft', 'is_featured',
        )

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    property = PropertyListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'property', 'created_at')
