from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Set a unique reverse name for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Set a unique reverse name for user permissions
        blank=True
    )
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self):
        return self.username

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science', 'Science'),
        ('Technology', 'Technology'),
        ('History', 'History'),
        ('Philosophy', 'Philosophy'),
        ('Art', 'Art'),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='book_covers/', null=False, blank=False, default='media/book_covers/1.jpg')
    is_available = models.BooleanField(default=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Fiction')

    def __str__(self):
        return self.title
    
    def is_issued(self):
        return IssuedBook.objects.filter(book=self, returned_on__isnull=True).exists()

class IssuedBook(models.Model):
    user = models.CharField(max_length=100)  # Store user name as a string
    phone_number = models.CharField(max_length=15)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    returned_on = models.DateField(null=True, blank=True)  # New field for the return date

    def mark_as_not_returned(self):
        self.returned_on = None  # Clear the returned date to mark it as not returned
        self.save()


    def __str__(self):
        return f"{self.user} - {self.book.title}"