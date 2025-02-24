from django.shortcuts import render, redirect
from django.contrib import messages
# from django.urls import reverse
from django.core.paginator import Paginator
from .models import Book, Category
import csv
from datetime import datetime

def home(request):
    """Home page"""
    # Get all books
    books = Book.objects.all()
    
    # Get filter parameters
    author_filter = request.GET.get('author', '')
    category_filter = request.GET.get('category', '')
    
    # Apply filters if provided
    if author_filter:
        books = books.filter(authors__icontains=author_filter)
    if category_filter:
        books = books.filter(category__name__icontains=category_filter)
    
    # Calculate total expenses by category
    category_expenses = {}
    for book in books:
        category_name = book.category.name if book.category else 'Uncategorized'
        category_expenses[category_name] = category_expenses.get(category_name, 0) + book.distribution_expense
    
    # Prepare data for pie chart
    labels = list(category_expenses.keys())
    values = list(category_expenses.values())
    
    context = {
        'labels': labels,
        'values': values,
        'authors': Book.objects.values_list('authors', flat=True).distinct(),
        'categories': Category.objects.all()
    }
    return render(request, 'home.html')
  
def book_list(request):
    """Display list of all books with pagination"""
    books = Book.objects.all().order_by('title')
    paginator = Paginator(books, 10)  # Show 10 books per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'book_list.html', {'page_obj': page_obj})