from django.contrib import admin
from .models import (
    User, Profile, Category, Skill, Service, Booking, Review,
    TrustBadge, Message, PaymentTransaction, EscrowTransaction, Location
)


admin.site.site_header = "SkillSwap Admin"
admin.site.site_title = "SkillSwap Portal"
admin.site.index_title = "Welcome to SkillSwap Admin Panel"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_provider', 'is_verified', 'is_staff')
    list_filter = ('is_provider', 'is_verified', 'is_staff')
    search_fields = ('username', 'email')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hourly_rate', 'rating')
    search_fields = ('user__username',)
    filter_horizontal = ('skills',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'price', 'service_type', 'payment_type', 'is_active')
    list_filter = ('service_type', 'payment_type', 'is_active')
    search_fields = ('title', 'provider__username')
    filter_horizontal = ('skills',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'service', 'status', 'scheduled_date', 'agreed_price')
    list_filter = ('status',)
    search_fields = ('client__username', 'service__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'provider', 'rating', 'created_at')
    search_fields = ('reviewer__username', 'provider__username')


@admin.register(TrustBadge)
class TrustBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'issuer', 'date_awarded')
    search_fields = ('user__username', 'title', 'issuer')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'created_at')
    search_fields = ('sender__username', 'recipient__username')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('booking__service__title', 'booking__client__username')


@admin.register(EscrowTransaction)
class EscrowTransactionAdmin(admin.ModelAdmin):
    list_display = ('payer', 'receiver', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('payer__username', 'receiver__username')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'country', 'postal_code')
    list_filter = ('country', 'state')
    search_fields = ('city', 'state', 'country')
