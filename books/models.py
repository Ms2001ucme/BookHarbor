from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, default=1, related_name="books")
    description = models.TextField(default="No description available.")
    published_date = models.DateField(default=timezone.now)
    cover_image = models.ImageField(upload_to="covers/", null=True, blank=True)

    # Google Books API fields
    google_book_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)

    # Watchlist & Favorites
    watchlist = models.ManyToManyField(User, related_name="watchlist_books", blank=True)
    favorites = models.ManyToManyField(User, related_name="favorite_books", blank=True)

    def __str__(self):
        return self.title

    def get_cover_image_url(self):
        """Return the best available cover image URL."""
        if self.cover_image and self.cover_image.name:
            return self.cover_image.url
        if self.thumbnail_url:
            return self.thumbnail_url
        return settings.STATIC_URL + "images/default_cover.png"



# Bookshelf Model (Corrected)

class Bookshelf(models.Model):
    CATEGORY_CHOICES = [
        ('reading', 'Currently Reading'),
        ('completed', 'Completed'),
        ('wishlist', 'Wishlist'),
        ('favorite', 'Favorite'),
        ('to-read', 'To Read'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="bookshelf_entries", null=True, blank=True)

    # Google Books API fields
    google_book_id = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='wishlist')
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'google_book_id'], name="unique_user_google_book"),
            models.UniqueConstraint(fields=['user', 'book'], name="unique_user_local_book")
        ]

    def __str__(self):
        book_title = self.title if self.title else "Untitled"
        return f"{self.user.username} - {book_title} ({self.get_category_display()})"



class BookList(models.Model):
    LIST_CHOICES = [
        ('favourite', 'Favourite'),
        ('to_read', 'To Read'),
        ('watchlist', 'Watchlist'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    google_book_id = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=300, blank=True)
    thumbnail = models.URLField(blank=True)
    list_type = models.CharField(max_length=20, choices=LIST_CHOICES)
    description = models.TextField(blank=True)
    preview_link = models.URLField(blank=True)
    read_link = models.URLField(blank=True)


    def __str__(self):
        return f"{self.title} - {self.list_type} - {self.user.username}"



