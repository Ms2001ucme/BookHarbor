from django.contrib import admin
from .models import Book,Category,Bookshelf,BookList

# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Bookshelf)
admin.site.register(BookList)