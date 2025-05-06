from django.db import models

MAX_LISTING_PHOTOS = 5  # Or however many you want

class ListingPhoto(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='listing_photos/')
    is_main = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'listing_photos'
        ordering = ['-is_main', 'uploaded_at']
