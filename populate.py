import os
import django
from datetime import date
from django.core.files import File
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')


# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_harbor.settings")  # Replace with your actual project name
django.setup()

from books.models import Book, Category  # Import Category model

# List of books to add
books_data = [
    # Fiction
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Fiction", "published_date": date(1960, 7, 11), "cover_image": "covers/mockingbird.jpg"},
    {"title": "1984", "author": "George Orwell", "category": "Fiction", "published_date": date(1949, 6, 8), "cover_image": "covers/1984.jpg"},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Fiction", "published_date": date(1925, 4, 10), "cover_image": "covers/gatsby.jpg"},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "category": "Fiction", "published_date": date(1813, 1, 28), "cover_image": "covers/pride.jpg"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Fiction", "published_date": date(1951, 7, 16), "cover_image": "covers/catcher.jpg"},

    # Science & Technology
    {"title": "A Brief History of Time", "author": "Stephen Hawking", "category": "Science & Technology", "published_date": date(1988, 4, 1), "cover_image": "covers/briefhistory.jpg"},
    {"title": "The Selfish Gene", "author": "Richard Dawkins", "category": "Science & Technology", "published_date": date(1976, 11, 30), "cover_image": "covers/selfishgene.jpg"},
    {"title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "category": "Science & Technology", "published_date": date(2011, 6, 1), "cover_image": "covers/sapiens.jpg"},
    {"title": "The Innovators", "author": "Walter Isaacson", "category": "Science & Technology", "published_date": date(2014, 10, 7), "cover_image": "covers/innovators.jpg"},
    {"title": "Clean Code", "author": "Robert C. Martin", "category": "Science & Technology", "published_date": date(2008, 8, 1), "cover_image": "covers/cleancode.jpg"},

    # History
    {"title": "The Diary of a Young Girl", "author": "Anne Frank", "category": "History", "published_date": date(1947, 6, 25), "cover_image": "covers/diary.jpg"},
    {"title": "Guns, Germs, and Steel", "author": "Jared Diamond", "category": "History", "published_date": date(1997, 3, 1), "cover_image": "covers/guns.jpg"},
    {"title": "The Wright Brothers", "author": "David McCullough", "category": "History", "published_date": date(2015, 5, 5), "cover_image": "covers/wright.jpg"},
    {"title": "The Silk Roads", "author": "Peter Frankopan", "category": "History", "published_date": date(2015, 8, 27), "cover_image": "covers/silkroads.jpg"},

    # Self-Help & Productivity
    {"title": "Atomic Habits", "author": "James Clear", "category": "Self-Help & Productivity", "published_date": date(2018, 10, 16), "cover_image": "covers/atomic.jpg"},
    {"title": "The 7 Habits of Highly Effective People", "author": "Stephen R. Covey", "category": "Self-Help & Productivity", "published_date": date(1989, 8, 15), "cover_image": "covers/7habits.jpg"},
    {"title": "Deep Work", "author": "Cal Newport", "category": "Self-Help & Productivity", "published_date": date(2016, 1, 5), "cover_image": "covers/deepwork.jpg"},
    {"title": "The Power of Now", "author": "Eckhart Tolle", "category": "Self-Help & Productivity", "published_date": date(1997, 1, 1), "cover_image": "covers/powernow.jpg"},
]

# Adding books to the database
for book in books_data:
    # Get or create the Category instance
    category_obj, _ = Category.objects.get_or_create(name=book["category"])

    # Create or update the book instance
    obj, created = Book.objects.get_or_create(
        title=book["title"],
        defaults={
            "author": book["author"],
            "category": category_obj,  # Assign the Category instance
            "published_date": book["published_date"],
        }
    )

    # Handle cover image
    if created:
        if book["cover_image"]:
            image_path = os.path.join("media", book["cover_image"])
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    obj.cover_image.save(os.path.basename(image_path), File(img_file))
        print(f"✅ Added: {book['title']}")
    else:
        print(f"⚠️ Skipped (already exists): {book['title']}")

print("🎉 Database populated successfully with books!")
