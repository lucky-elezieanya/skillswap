from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta


# 1. User
class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_provider = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    community_verified = models.BooleanField(default=False)
    video_intro_url = models.URLField(blank=True, null=True)

    
    REQUIRED_FIELDS = []  # or other required fields

    def __str__(self):
        return f"{self.username} ({'Provider' if self.is_provider else 'Client'})"

# 2. Profile
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    languages = models.CharField(max_length=255, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    skills = models.ManyToManyField('Skill', blank=True)
    rating = models.FloatField(default=0.0)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# 3. Category & Skill
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


# 4. Service
SERVICE_TYPES = [
    ('digital', 'Digital'),
    ('local', 'Local/In-person'),
]

PAYMENT_TYPES = [
    ('escrow', 'Escrow'),
    ('postpay', 'Pay After Service'),
    ('barter', 'Barter'),
]

class Service(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f"{self.title} by {self.provider.username}"


# 5. Booking
BOOKING_STATUS = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

class Booking(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    scheduled_date = models.DateTimeField(null=True, blank=True)
    message = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    agreed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_barter = models.BooleanField(default=False)
    barter_offer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.client.username} → {self.service.title}"

# 6. Review
class Review(models.Model):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reviews')
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}⭐ from {self.reviewer.username} to {self.provider.username}"

# 7. TrustBadge
class TrustBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    issuer = models.CharField(max_length=100)  # Could be a community, church, etc.
    description = models.TextField(blank=True)
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

# 8. Message
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField(blank=True)
    audio_note = models.FileField(upload_to='audio_notes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"


# 9. PaymentTransaction
TRANSACTION_STATUS = [
    ('initiated', 'Initiated'),
    ('held', 'Held in Escrow'),
    ('released', 'Released to Provider'),
    ('refunded', 'Refunded'),
]

class PaymentTransaction(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.booking.id} - {self.status}"

# Escrow Transaction
class EscrowTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('released', 'Released'),
        ('refunded', 'Refunded'),
        ('disputed', 'Disputed'),
    ]

    payer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='escrow_payments', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='escrow_receipts', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, help_text="Description of the service or agreement")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    released_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    service_id = models.UUIDField(null=True, blank=True, help_text="Optional reference to a service request")
    released = models.BooleanField(default=False)
    disputed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Escrow from {self.payer} to {self.receiver} - {self.status} - ₦{self.amount}"

    def release_funds(self):
        """Mark the escrow as released and record time."""
        self.status = 'released'
        self.released_at = timezone.now()
        self.save()

    def refund_funds(self):
        """Mark the escrow as refunded and record time."""
        self.status = 'refunded'
        self.refunded_at = timezone.now()
        self.save()

    def is_releasable(self):
        """Logic to determine if funds can be released (e.g., service complete)."""
        return self.status == 'pending'

    def save(self, *args, **kwargs):
        if not self.released_at:
            self.released_at = timezone.now() + timedelta(days=7)  # auto release in 7 days
        super().save(*args, **kwargs)

# 11. Location
class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['country', 'state', 'city']
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.city}, {self.state or ''}, {self.country}"
