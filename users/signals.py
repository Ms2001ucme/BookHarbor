from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CompletedBook, ReadingChallenge

@receiver(post_save, sender=CompletedBook)
def update_reading_progress(sender, instance, created, **kwargs):
    """Update the books_read count when a user completes a book."""
    if created:  # Only update if a new completed book is added
        challenge = ReadingChallenge.objects.filter(user=instance.user).order_by('-end_date').first()
        if challenge:
            challenge.books_read += 1
            challenge.save()
