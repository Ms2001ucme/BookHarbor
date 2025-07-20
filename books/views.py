from django.shortcuts import render,redirect,get_object_or_404
from .models import Book,BookList
from .forms import BookForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reviews.models import Review
from reviews.forms import ReviewForm
from django.db.models import Q
import requests
from django.shortcuts import render
from django.conf import settings
import os



def get_google_books_data(title, max_results=10, start_index=0):
    """
    Fetch book details from Google Books API.
    
    :param title: Title of the book to search.
    :param max_results: Number of results to return.
    :param start_index: Pagination index for fetching more results.
    :return: List of books with relevant details.
    """
    GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY", settings.GOOGLE_BOOKS_API_KEY)
    url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}&key={GOOGLE_BOOKS_API_KEY}&maxResults={max_results}&startIndex={start_index}"

    try:
        response = requests.get(url, timeout=5)  # ✅ Set timeout to prevent slow API responses
        response.raise_for_status()  # ✅ Raise an error for HTTP 4xx/5xx responses

        data = response.json()

        if "items" not in data:
            return []  # ✅ Return empty list if no books found

        books = []
        for item in data["items"]:
            volume_info = item.get("volumeInfo", {})
            book_id = item.get("id")  # ✅ Extract the Google Book ID

            if not book_id:  # ✅ Ensure book has an ID
                continue  

            books.append({
                "id": book_id,  # REQUIRED for linking to the detail page
                "title": volume_info.get("title", "Unknown Title"),
                "author": ", ".join(volume_info.get("authors", ["Unknown Author"])),
                "description": volume_info.get("description", "No description available."),
                "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                "google_books_url": volume_info.get("infoLink", "#"),
                "preview_link": volume_info.get("previewLink", ""),  # ✅ Add preview link
                "published_date": volume_info.get("publishedDate", "Unknown"),
                "page_count": volume_info.get("pageCount", "N/A"),
                "categories": volume_info.get("categories", ["Uncategorized"]),
            })

        return books

    except requests.exceptions.RequestException as e:
        print(f"Google Books API Error: {e}")
        return []



def search_books(request):
    query = request.GET.get("q", "").strip()
    
    local_books = []
    google_books = []

    if query:
        # Search local books (case insensitive)
        local_books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query)
        )
        
        # Fetch from Google Books API
        google_books = get_google_books_data(query)

    return render(request, "books/search_results.html", {
        "query": query,
        "local_books": local_books,
        "google_books": google_books,
    })


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to book list after saving
    else:
        form = BookForm()

    return render(request, 'books/add_book.html', {'form': form})


    # Get all bookshelf entries for the logged-in user
    bookshelf_entries = Bookshelf.objects.filter(user=request.user)

    # Group books by category (Reading, Completed, Wishlist)
    grouped_books = {}
    for entry in bookshelf_entries:
        category = entry.get_category_display()  # Get human-readable category name
        if category not in grouped_books:
            grouped_books[category] = []

        book_data = {
            "title": entry.title,
            "author": entry.author or "Unknown Author",
            "category": category,
            "cover_url": entry.thumbnail_url if entry.thumbnail_url else "/static/images/default_cover.png",
            "book_id": entry.book.id if entry.book else None,  # Check if book exists
            "google_book_id": entry.google_book_id,
        }
        grouped_books[category].append(book_data)

    return render(request, "books/bookshelf.html", {"grouped_books": grouped_books})








    """Add a book to the user's favorites."""
    book = get_object_or_404(Book, id=book_id)
    
    # Check if the book is already in favorites
    favorite, created = Bookshelf.objects.get_or_create(user=request.user, book=book, category="favorites")

    if created:
        messages.success(request, f"Added '{book.title}' to Favorites!")
    else:
        messages.info(request, f"'{book.title}' is already in your Favorites.")

    return redirect("book_detail", book_id=book.id)



GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes/"

@login_required
def google_book_detail(request, book_id):
    """Fetch and display Google Book details + handle reviews."""
    GOOGLE_BOOKS_API_KEY = settings.GOOGLE_BOOKS_API_KEY
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}?key={GOOGLE_BOOKS_API_KEY}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            book_data = response.json()
            volume_info = book_data.get("volumeInfo", {})
            access_info = book_data.get("accessInfo", {})

            book = {
                "id": book_data.get("id"),
                "title": volume_info.get("title", "Unknown Title"),
                "author": ", ".join(volume_info.get("authors", ["Unknown Author"])),
                "description": volume_info.get("description", "No description available."),
                "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                "published_date": volume_info.get("publishedDate", "Unknown Date"),
                "google_books_url": volume_info.get("infoLink", "#"),
                "preview_link": volume_info.get("previewLink", ""),
                "web_reader_link": access_info.get("webReaderLink", ""),
                "is_readable": access_info.get("viewability") in ["FULL", "PARTIAL"],
                "rating": volume_info.get("averageRating"),
                "pageCount": volume_info.get("pageCount"),
                "categories": volume_info.get("categories", []),
                "publisher": volume_info.get("publisher"),
                "language": volume_info.get("language"),
            }
            
            form = ReviewForm()
            if request.method == "POST":
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.user = request.user
                    review.google_book_id = book_id
                    review.save()
                    return redirect("google_book_detail", book_id=book_id)
                else:
                    messages.error(request, 'There was an error with your review.')

            reviews = Review.objects.filter(google_book_id=book_id).order_by('-created_at')

            return render(request, "books/google_book_detail.html", {
                "book": book,
                "form": form,
                "reviews": reviews,
            })

    except Exception as e:
        print(f"❌ Exception: {e}")

    messages.error(request, "Book details not available.")
    return redirect("search_books")




@login_required
def add_to_list(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        title = request.POST.get("title")
        authors = request.POST.get("authors")
        thumbnail = request.POST.get("thumbnail")
        list_type = request.POST.get("list_type")

        # Avoid duplicate entries
        exists = BookList.objects.filter(
            user=request.user,
            google_book_id=book_id,
            list_type=list_type
        ).exists()

        if not exists:
            BookList.objects.create(
                user=request.user,
                google_book_id=book_id,
                title=title,
                authors=authors,
                thumbnail=thumbnail,
                list_type=list_type
            )
    return redirect(request.META.get('HTTP_REFERER', 'home'))



@login_required
def my_book_lists(request):
    def serialize_booklist(booklist_queryset):
        return [
            {
                'id': b.google_book_id,  # ✅ This will fix your detail view URL
                'title': b.title,
                'authors': b.authors,
                'thumbnail': b.thumbnail,  
            
            }
            for b in booklist_queryset
        ]

    grouped_books = [
        {'name': 'Reading', 'books': serialize_booklist(BookList.objects.filter(user=request.user, list_type='reading'))},
        {'name': 'Favourite', 'books': serialize_booklist(BookList.objects.filter(user=request.user, list_type='favourite'))},
        {'name': 'Watchlist', 'books': serialize_booklist(BookList.objects.filter(user=request.user, list_type='watchlist'))},
    ]
    
    return render(request, 'users/my_list.html', {'grouped_books': grouped_books})




@login_required
def remove_from_list(request, book_id):
    BookList.objects.filter(id=book_id, user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER', 'my_book_lists'))


def filter_books_by_category(request):
    selected_category = request.GET.get('category', 'Fiction')  # Default to Fiction
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{selected_category}&maxResults=20'
    response = requests.get(url)
    
    books = []
    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            volume = item.get('volumeInfo', {})
            access = item.get('accessInfo', {})

            books.append({
                'id': item.get('id'),
                'title': volume.get('title'),
                'authors': volume.get('authors', []),
                'description': volume.get('description', 'No description available.'),
                'thumbnail': volume.get('imageLinks', {}).get('thumbnail', ''),
                'previewLink': volume.get('previewLink'),
                'readable': access.get('viewability') in ['ALL_PAGES', 'FULL'],
                'readLink': access.get('webReaderLink'),
            })

    categories = ['Fiction', 'Science', 'History', 'Romance', 'Fantasy', 'Mystery']
    return render(request, 'books/category_filter.html', {
        'books': books,
        'categories': categories,
        'selected_category': selected_category,
    })

@login_required
def view_group_books(request, group_name):
    # Normalize group name if needed
    group_name_lower = group_name.lower()
    valid_groups = ['favourite', 'to_read', 'watchlist']

    if group_name_lower not in valid_groups:
        messages.error(request, "Invalid book list type.")
        return redirect('my_book_lists')

    books = BookList.objects.filter(user=request.user, list_type=group_name_lower)

    return render(request, 'books/group_books.html', {
        'group_name': group_name,
        'books': books,
    })

