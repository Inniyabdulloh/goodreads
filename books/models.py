from django.utils import timezone

from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    cover_pic = models.ImageField(default='default-book.png')
    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book} by {self.author}"

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stars_given} by {self.user.username} for {self.book}"