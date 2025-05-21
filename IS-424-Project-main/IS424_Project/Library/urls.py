# Library/urls.py
from django.urls import path
from . import views

app_name = "Library"  # Ensure the app_name is set correctly

urlpatterns = [
    path('', views.menu, name='menu'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'), 
    path('add/', views.addBook, name='add'),
    path('delete', views.deleteBook, name='delete'),
    path('allBooks/', views.allBooks, name='allBooks'),
    path('specificBook/<int:book_id>/', views.specificBook, name='specificBook'),
    path('update_book/', views.update_book, name='update_book'),
]

