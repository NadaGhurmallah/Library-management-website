# Library/models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return self.username
 
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    published_date = models.DateField()
    reserved_by = models.ManyToManyField(User, related_name='reserved_books', blank=True)

    def _str_(self):
        return self.title
