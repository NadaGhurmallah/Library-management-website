# Library/models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return self.username
 
class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=150)
    genre = models.CharField(max_length=150)

    def __str__(self):
        return self.title
