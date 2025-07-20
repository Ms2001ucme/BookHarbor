from django.urls import path
from . import views


urlpatterns = [
    path('my-lists/', views.my_book_lists, name='my_book_lists'),
    path('add-to-list/', views.add_to_list, name='add_to_list'),
    path('remove-from-list/<int:book_id>/', views.remove_from_list, name='remove_from_list'),
    path('google-book/<str:book_id>/', views.google_book_detail, name='google_book_detail'),
    path('category-filter/', views.filter_books_by_category, name='category_filter'),
    path('books/group/<str:group_name>/', views.view_group_books, name='view_group_books'),



    # ✅ Searching and Categories
    path("search/", views.search_books, name="search_books"),


]

