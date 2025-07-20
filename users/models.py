from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.apps import apps  # ✅ Lazy import to avoid circular dependency

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('author', 'Author'),
    )

    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True,default='profile_pics/default.png')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def is_author(self):
        return self.role == 'author'

    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return f"{self.username} ({self.role})"

User = get_user_model()

class ReadingChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reading_challenges")
    goal = models.PositiveIntegerField()  # Total books to read
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    books_read = models.PositiveIntegerField(default=0)
    books = models.ManyToManyField("books.Book", blank=True)  # ✅ Track books in challenge


    def progress(self):
        """Calculate completion percentage."""
        return (self.books_read / self.goal) * 100 if self.goal > 0 else 0

    def __str__(self):
        return f"{self.user.username} - {self.goal} books by {self.end_date}"

class CompletedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="completed_books")
    book_id = models.PositiveIntegerField()  # ✅ Store book ID instead of a ForeignKey to avoid import issues
    completed_date = models.DateField(default=timezone.now)

    def get_book(self):
        """Dynamically get the book instance to avoid circular imports."""
        Book = apps.get_model("books", "Book")  # ✅ Lazy import
        return Book.objects.get(id=self.book_id)

    def __str__(self):
        return f"{self.user.username} completed {self.get_book().title}"
    


