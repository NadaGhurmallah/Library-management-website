from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Book, User
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import messages

def menu(request, username):
    try:
        user = User.objects.get(username=username)
        books = Book.objects.filter(user=user)     
        return render(request, 'Library/menu.html', {'books': books, 'username': username})

    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('Library:login') 




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                # Set a session variable to track the user's login state
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                messages.success(request, "Login successful!")
                return redirect('Library:menu', username=user.username)
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
            messages.error(request, 'Username already exists.')
            return render(request, 'Library/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'Library/register.html')

        hashed_password = make_password(password)

        new_user = User(username=username, password=hashed_password, email=email)
        new_user.save()

        return redirect('Library:menu', username=username)

    return render(request, 'Library/register.html')





def all_books(request, username):
    books = Book.objects.filter(user__username=username)
    return render(request, 'Library/allBooks.html', {'books': books, 'username': username})




def specificBook(request, book_id, username):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('Library:menu', username=username)

    user_id = request.session.get('user_id')
    session_username = request.session.get('username')

    if not user_id or session_username != username:
        messages.error(request, "You must be logged in to reserve a book.")
        return redirect('Library:login')

    is_reserved = book.reserved_by.filter(id=user_id).exists()

    if request.method == 'POST':
        if not is_reserved:
           
            book.reserved_by.add(User.objects.get(id=user_id))
            messages.success(request, "You have successfully reserved this book.")
            return redirect('Library:specificBook', book_id=book.id, username=username)
        else:
            messages.error(request, "You have already reserved this book.")

    return render(request, 'Library/specificBook.html', {
        'book': book,
        'username': username,
        'is_reserved': is_reserved
    })


def addbook(request, username):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        genre = request.POST['genre']
        published_date = request.POST['published_date']
        
        try:
            user = User.objects.get(username=username)
            new_book = Book(title=title, author=author, genre=genre, published_date=published_date, user=user)
            new_book.save()
            return redirect('Library:menu', username=username)  # Redirect back to the menu with the username
        except User.DoesNotExist:
            return redirect('Library:login')  # Handle case where user does not exist

    return render(request, 'Library/addbook.html',{'username': username})




from django.shortcuts import render, get_object_or_404, redirect
from .models import Book

def update_book(request, username, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.genre=request.POST.get('genre')
        book.published_date=request.POST.get('published_date')
        book.save()
        return redirect('Library:all_books', username=username)  

    return render(request, 'Library/update_book.html', {'book': book, 'username': username})




def deleteBook(request,username,  book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully!")
        return redirect('Library:all_books', username=username)  

    return render(request, 'Library/deleteBook.html', {'book': book, 'username': username})




def logout_view(request):
    request.session.flush() 
    messages.success(request, "You have successfully logged out.")
    return redirect('Library:login')  

