
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reserved_books')


    def __str__(self):
        return self.title
