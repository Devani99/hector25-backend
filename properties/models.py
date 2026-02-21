from django.db import models
from django.conf import settings


class Property(models.Model):
    """A property listing (house, apartment, villa, office)."""

    TYPE_CHOICES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Office', 'Office'),
    ]
    LISTING_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('rent', 'Rent'),
        ('new_launch', 'New Launch'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='properties',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES, default='buy')
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqft = models.PositiveIntegerField(default=0, help_text='Area in square feet')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.location}"


class PropertyImage(models.Model):
    """Images associated with a property."""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image #{self.order} for {self.property.title}"


class Amenity(models.Model):
    """Amenities (e.g., Pool, Gym, Parking) for a property."""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='amenities')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text='Icon identifier, e.g. pool, gym')

    def __str__(self):
        return f"{self.name} — {self.property.title}"


class Favorite(models.Model):
    """A user's favorited property."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites'
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.email} ♡ {self.property.title}"
