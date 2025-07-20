from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm,ProfileUpdateForm
from django.contrib import messages
from books.models import Book,Bookshelf
from .models import ReadingChallenge
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from collections import defaultdict
from .models import ReadingChallenge
import requests
from django.core.paginator import Paginator

def home(request):
    query = request.GET.get("q", "fiction")
    readable_only = request.GET.get("readable_only") == "on"
    books = []

    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=40'  # You can increase maxResults if needed (max is 40)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            volume = item.get('volumeInfo', {})
            access = item.get('accessInfo', {})
            readable = access.get('viewability') in ['ALL_PAGES', 'FULL']

            if readable_only and not readable:
                continue

            books.append({
                'id': item.get('id'),
                'title': volume.get('title'),
                'authors': volume.get('authors', []),
                'description': volume.get('description', 'No description available.'),
                'thumbnail': volume.get('imageLinks', {}).get('thumbnail', ''),
                'previewLink': volume.get('previewLink'),
                'readable': readable,
                'readLink': access.get('webReaderLink'),
                'rating': volume.get('averageRating'),
                'pageCount': volume.get('pageCount'),
            })

    # Paginate the books list
    paginator = Paginator(books, 12)  # Show 8 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'query': query,
        'readable_only': readable_only
    })




def about_view(request):
    return render(request,'about.html')

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, "Registration successful! Welcome to Book Harbor.")

            # Redirect based on user role
            if user.is_author():
                return redirect("author_dashboard")
            return redirect("user_dashboard")
        else:
            messages.error(request, "There was an issue with your registration. Please try again.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "users/join.html", {"form": form})

# User Login View
User = get_user_model()

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")  # Username is actually email
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)  # Find user by email
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")

                # Redirect to role-based dashboards
                if user.is_author():
                    return redirect("home")
                return redirect("home")

            else:
                messages.error(request, "Invalid email or password. Please try again.")
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")

    form = AuthenticationForm()
    return render(request, "users/sign_in.html", {"form": form})

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

def role_based_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_author():
            return redirect('author_dashboard')
        return redirect('user_dashboard')
    return redirect('login')

@login_required
def author_dashboard(request):
    if not request.user.is_author():
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, "users/author_dashboard.html")

@login_required
def user_dashboard(request):
    if not request.user.is_user():
        return HttpResponseForbidden("You are not authorized to access this page.")

    # Fetch books in the user's watchlist
    watchlist = Bookshelf.objects.filter(user=request.user, category="watchlist").select_related("book")

    # Get user's favorite categories from books in their watchlist
    user_categories = watchlist.values_list("book__category_id", flat=True).distinct()

    # Recommend books from the same category (excluding user's books)
    recommended_books = Book.objects.filter(category_id__in=user_categories).exclude(
        id__in=watchlist.values_list("book__id", flat=True)
    ).order_by("?")[:5]  # Pick 5 random books

    context = {
        "watchlist": watchlist,
        "recommended_books": recommended_books,
    }

    return render(request, "users/user_dashboard.html", context)


@login_required
def user_profile(request):
    """Display user profile with bookshelf books categorized by type."""
    user = request.user
    bookshelf_entries = Bookshelf.objects.filter(user=user).select_related("book")

    # Group books by category (watchlist, favorites, etc.)
    bookshelf_books = defaultdict(list)
    for entry in bookshelf_entries:
        bookshelf_books[entry.category].append(entry.book)

    # Get favorite books separately
    favorite_books = bookshelf_books.get("favorites", [])

    context = {
        "user": user,
        "bookshelf_books": dict(bookshelf_books),  # Convert defaultdict to dict
        "favorite_books": favorite_books,
    }
    return render(request, "users/profile.html", context)



@login_required
def profile_update(request):
    """Allow users to update their profile (picture & details)."""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("user_profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "users/profile_update.html", {"form": form})


@login_required
def bookshelf_view(request):
    bookshelf_books = Bookshelf.objects.filter(user=request.user)
    challenge = ReadingChallenge.objects.filter(user=request.user).order_by('-end_date').first()

    return render(request, 'books/bookshelf.html', {'bookshelf_books': bookshelf_books, 'challenge': challenge})




