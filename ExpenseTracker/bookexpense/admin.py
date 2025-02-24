from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Book, Category
import csv
from datetime import datetime

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'publisher', 'published_date', 'get_category', 'distribution_expense')
    list_filter = ('category', 'publisher')
    search_fields = ('title', 'authors', 'publisher')
    
    def get_category(self, obj):
        return obj.category.name if obj.category else '-'
    get_category.short_description = 'Category'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='book_import_csv'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("csv_file")
            if not csv_file:
                self.message_user(request, 'No file uploaded', level='error')
                return HttpResponseRedirect("../")
                
            if not csv_file.name.endswith('.csv'):
                self.message_user(request, 'Wrong file type', level='error')
                return HttpResponseRedirect("../")

            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                try:
                    # Get or create category
                    category, _ = Category.objects.get_or_create(
                        name=row['category']
                    )
                    
                    # Create book with category relationship
                    Book.objects.create(
                        id=row['id'],
                        title=row['title'],
                        subtitle=row['subtitle'] if row['subtitle'] else None,
                        authors=row['authors'],
                        publisher=row['publisher'],
                        published_date=datetime.strptime(row['published_date'], '%Y-%m-%d').date(),
                        category=category,
                        distribution_expense=float(row['distribution_expense'])
                    )
                except Exception as e:
                    self.message_user(request, f'Error importing row: {e}', level='error')
                    continue

            self.message_user(request, 'CSV file imported successfully')
            return HttpResponseRedirect("../")

        context = {
            'title': 'Import CSV',
            'app_label': 'bookexpense',
            'opts': self.model._meta,
            'has_permission': self.has_change_permission(request),
        }
        return render(request, 'admin/csv_import.html', context)