from django.db import models
from django.contrib.auth.models import User
from pet_welfare.models import Listing

class ListingBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_listings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookmarks')
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        db_table = 'listing_bookmarks'
