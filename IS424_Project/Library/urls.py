from django.urls import path
from . import views

app_name = "Library" 

urlpatterns = [
    path('menu/<str:username>/', views.menu, name='menu'),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('add/<str:username>/', views.addbook, name='addbook'),
    path('deleteBooks/<str:username>/<int:book_id>/', views.deleteBook, name='deleteBook'), 
    path('allBooks/<str:username>/', views.all_books, name='all_books'),
    path('specificBook/<str:username>/<int:book_id>/', views.specificBook, name='specificBook'),
    path('update_book/<str:username>/<int:book_id>/', views.update_book, name='update_book'), 
    path('logout/',views.logout_view , name='logout')
]


