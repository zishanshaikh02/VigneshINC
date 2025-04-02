from django.urls import path
from .views import book_list_create, book_detail, rent_book, return_book

urlpatterns = [
    path('books/', book_list_create, name='book-list-create'),
    path('books/<int:pk>/', book_detail, name='book-detail'),
    path('books/<int:book_id>/rent/', rent_book, name='rent-book'),
    path('books/<int:book_id>/return/', return_book, name='return-book'),
]
