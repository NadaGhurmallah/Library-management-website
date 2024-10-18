# Library/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import User



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
