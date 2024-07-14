from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields you want here
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username

class ExtractedText(models.Model):
    text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]