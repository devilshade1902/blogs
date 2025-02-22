from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

class Author(AbstractUser):
    email = models.EmailField(unique=True)  # Use 'email' instead of 'email1'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'  # Use email instead of username for authentication
    REQUIRED_FIELDS = ['email']  # Required fields other than email

    def __str__(self):
        return self.email