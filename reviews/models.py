from django.db import models
from django.conf import settings  # Import settings to use custom user model
from django.core.validators import MinValueValidator, MaxValueValidator
from books.models import Book

# Review Model
class Review(models.Model):
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE, null=True, blank=True)  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use custom user model
    google_book_id = models.CharField(max_length=100, blank=True, null=True)  # Add this
    content = models.TextField()  
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Restrict rating to 1-5
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title} (Rating: {self.rating})"
