# Library/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import User , Book
from django.http import HttpRequest



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                # Login successful
                messages.success(request, "Login successful!")
                return redirect('home')  
            else:
                messages.error(request, "Incorrect password.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, 'Library/login.html') 


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  

        if User.objects.filter(username=username).exists():
            return render(request, 'Library/register.html', {'error': 'Username already exists.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'Library/register.html', {'error': 'Email already exists.'})

        
        hashed_password = make_password(password)

        
        new_user = User(username=username, password=hashed_password, email=email)
        new_user.save()
        
        return redirect('login')  

    return render(request, 'Library/register.html')

def home(request):
    return render(request, 'Library/home.html') 

def addBook(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        published_date = request.POST.get('published_date')

        book = Book(title=title, author=author, genre=genre, published_date=published_date)
        book.save()
        
        return redirect('view_books')  # Redirect to view that shows all books############
    return render(request, 'addBook.html')


def deleteBook(request):
    if request.method == "POST":
        title = request.POST.get('title')
        
        try:
            book = Book.objects.get(title=title)
            book.delete()
            return redirect('view_books')  # Redirect to list of books##########
        except Book.DoesNotExist:
            return render(request, 'deleteBook.html', {'error': 'Book not found'})
    
    return render(request, 'deleteBook.html')

def allBooks(request):
    books = Book.objects.all()  
    return render(request, 'Library/allBooks.html', {'books': books})

def specificBook(request, book_id):
    try:
        book = Book.objects.get(id=book_id) 
        if request.method == "POST" and 'reserve' in request.POST:
            book.reserved_by.add(request.user)
            book.save()
            return redirect('library:specificBook', book_id=book_id)
            
    except Book.DoesNotExist: #book not found
        return render(request, 'Library/allBooks.html', {'error': 'Book not found'})
