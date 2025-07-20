import os
import django
import random
from datetime import datetime

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_harbor.settings")
django.setup()

from django.contrib.auth import get_user_model
from books.models import Book  # Ensure Review model is imported
from reviews.models import Review

# Get the custom user model
User = get_user_model()

# Debugging check
print(f"Using User model: {User}")

# List of users to add reviews
users_data = [
    {"username": "asmit", "email": "asmit@example.com"},
    {"username": "mohit", "email": "mohit@example.com"},
    {"username": "john", "email": "john@example.com"},
    {"username": "emma", "email": "emma@example.com"},
]

# Possible review comments
review_texts = [
    "An amazing read! Highly recommend.",
    "Very insightful and well-written.",
    "A book that everyone should read at least once.",
    "Couldn’t put it down! Fantastic storytelling.",
    "A great book with deep insights.",
]

# Possible ratings (ensuring they are between 1 and 5)
ratings = [1, 2, 3, 4, 5]

# Step 1: Create or get users
users = []
for user_data in users_data:
    user, created = User.objects.get_or_create(username=user_data["username"], defaults={"email": user_data["email"]})
    users.append(user)

# Step 2: Fetch all books
books = Book.objects.all()

# Step 3: Create reviews
try:
    for user in users:
        for book in books:
            # Check if review already exists
            if not Review.objects.filter(book=book, user=user).exists():
                Review.objects.create(
                    book=book,
                    user=user,
                    rating=random.choice(ratings),
                    content=random.choice(review_texts),  # Use 'content' instead of 'comment'
                    created_at=datetime.now(),
                )
                print(f"✅ Review added: {user.username} → {book.title}")
            else:
                print(f"⚠️ Skipping (already exists): {user.username} → {book.title}")

    print("🎉 Reviews added successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
