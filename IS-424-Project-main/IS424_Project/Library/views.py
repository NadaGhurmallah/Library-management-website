# Library/views.py
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import User , Book
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse

def menu(request):
    return render(request, 'Library/menu.html') 


def login_view(request):#requirement 1
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


def register_view(request):#requirement 2
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


def allBooks(request):#requirement 4
    books = Book.objects.all()  
    return render(request, 'Library/allBooks.html', {'books': books})

def specificBook(request, book_id):#requirement 5
    try:
        book = Book.objects.get(id=book_id) 
        return render(request, 'Library/specificBook.html', {'book': book})
    except Book.DoesNotExist: #book not found
        return render(request, 'Library/allBooks.html', {'error': 'Book not found'})
    
def addBook(request):#requirement 6
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        published_date = request.POST.get('published_date')

        book = Book(title=title, author=author, genre=genre, published_date=published_date)
        book.save()
        
        return redirect('view_books')  # Redirect to view that shows all books############
    return render(request, 'addBook.html')

def update_book(request):  
    if request.method == "POST":
        title = request.POST.get('title') 
        book = get_object_or_404(Book, title=title)  # Retrieve the book by title
        
        # Update the book's details
        book.author = request.POST.get('author', book.author)
        book.publication_date = request.POST.get('publication_date', book.publication_date)
        book.genre = request.POST.get('genre', book.genre)
        book.save()
        
        return render(request, 'Library/specificBook.html', {'book': book})  # Redirect to the updated book's details

    else: 
        # Handle GET request to show the form with pre-filled book details
        title = request.GET.get('title')  # Get title from query params for the book to update
        book = get_object_or_404(Book, title=title)  # Ensure the book exists
        
        return render(request, "Library/update_book.html", {"book": book})  # Render update form with book details



def deleteBook(request):#requirement 8
    if request.method == "POST":
        title = request.POST.get('title')

        
        try:
            book = Book.objects.get(title=title)
            book.delete()
            return redirect('view_books')  # Redirect to list of books##########
        except Book.DoesNotExist:
            return render(request, 'deleteBook.html', {'error': 'Book not found'})
    
    return render(request, 'deleteBook.html')


    

