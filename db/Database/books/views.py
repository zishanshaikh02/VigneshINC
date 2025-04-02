from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, permissions
from django.utils.timezone import now
from .models import Book, Rental
from .serializers import BookSerializer, RentalSerializer

# ✅ List and Create Books (with Pagination & Filtering)
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])  # For file upload
# @permission_classes([permissions.IsAuthenticated])
def book_list_create(request):
    if request.method == 'GET':
        books = Book.objects.all()

        # ✅ Filtering
        title = request.GET.get('title', None)
        author = request.GET.get('author', None)
        is_available = request.GET.get('is_available', None)

        if title:
            books = books.filter(title__icontains=title)
        if author:
            books = books.filter(author__icontains=author)
        if is_available is not None:
            books = books.filter(is_available=is_available.lower() == 'true')

        # ✅ Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Default page size
        paginated_books = paginator.paginate_queryset(books, request)

        serializer = BookSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Retrieve, Update, Delete a Book
@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([permissions.IsAuthenticated])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data, partial=True)  # Partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# ✅ Rent a Book
@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def rent_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not book.is_available:
        return Response({"error": "Book is already rented"}, status=status.HTTP_400_BAD_REQUEST)

    rental = Rental.objects.create(user=request.user, book=book)
    book.is_available = False
    book.save()
    
    serializer = RentalSerializer(rental)
    return Response({"message": "Book rented successfully", "rental": serializer.data}, status=status.HTTP_201_CREATED)

# ✅ Return a Book
@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def return_book(request, book_id):
    rental = Rental.objects.filter(user=request.user, book_id=book_id, returned_at__isnull=True).first()

    if not rental:
        return Response({"error": "No active rental found"}, status=status.HTTP_400_BAD_REQUEST)

    rental.returned_at = now()
    rental.book.is_available = True
    rental.book.save()
    rental.save()

    return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)
