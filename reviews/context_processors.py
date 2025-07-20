# In context_processors.py
from books.models import Category

def categories(request):
    return {
        'categories': Category.objects.all()
    }
