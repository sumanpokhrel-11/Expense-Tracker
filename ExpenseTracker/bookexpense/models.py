from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Book(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=255)
    subtitle = models.TextField(null=True, blank=True)
    authors = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    published_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    distribution_expense = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']