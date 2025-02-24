from django.urls import path
from . import views

app_name = 'bookexpense'

urlpatterns = [
    path('', views.home, name='home'),
    # path('import/', views.import_books, name='import'),
    # path('book/<str:book_id>/', views.book_detail, name='book_detail'),
    path('booklist/', views.book_list, name='book_list'),

]