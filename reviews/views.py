from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from books.models import Book,Category
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {'form': form, 'book': book})

def books_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category=category)
    for book in books:
        if not book.cover_image:
            book.cover_image = "covers/default.png"  # Ensure this exists in /media/covers/

    context = {'category': category, 'books': books}
    return render(request, 'books/books_by_category.html',context )

