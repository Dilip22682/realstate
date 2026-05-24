from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('customer', 'Customer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return self.username

 

class Property(models.Model):

    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('commercial', 'Commercial'),
    ]

    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title       = models.CharField(max_length=200)
    description = models.TextField()
    location    = models.CharField(max_length=200)
    price       = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms    = models.IntegerField()
    bathrooms   = models.IntegerField()
    area        = models.IntegerField()
    image       = models.ImageField(upload_to='properties/')
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    property    = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    name        = models.CharField(max_length=100)
    email       = models.EmailField()
    phone       = models.CharField(max_length=15)
    message     = models.TextField(blank=True, null=True)
    date        = models.DateField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"

    class Meta:
        ordering = ['-created_at']  # latest bookings first