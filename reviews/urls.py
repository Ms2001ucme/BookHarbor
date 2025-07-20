from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('books/<int:book_id>/add_review/', views.add_review, name='add_review'),
    path('reviews_list/', views.review_list, name='review_list'),
    path('category/<int:category_id>/', views.books_by_category, name='books_by_category'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)