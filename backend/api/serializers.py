from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Profile, Skill, Category, Service, Booking,
    Review, TrustBadge, Message, PaymentTransaction, EscrowTransaction, Location
)

User = get_user_model()
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'phone', 'location', 'is_provider']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data.get('username', ''),
            phone=validated_data.get('phone', ''),
            location=validated_data.get('location', ''),
            is_provider=validated_data.get('is_provider', False),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# --- 1. UserSerializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'location', 'is_provider', 'is_verified',
            'community_verified', 'video_intro_url'
        ]


# --- 2. ProfileSerializer ---
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'bio', 'languages',
            'hourly_rate', 'skills', 'rating', 'profile_picture'
        ]


# --- 3. CategorySerializer ---
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# --- 4. SkillSerializer ---
class SkillSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category', queryset=Category.objects.all(), write_only=True
    )

    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'category_id']


# --- 5. ServiceSerializer ---
class ServiceSerializer(serializers.ModelSerializer):
    provider = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), many=True, write_only=True, source='skills'
    )

    class Meta:
        model = Service
        fields = [
            'id', 'provider', 'title', 'description',
            'service_type', 'payment_type', 'price',
            'is_active', 'created_at', 'skills', 'skill_ids'
        ]


# --- 6. BookingSerializer ---
class BookingSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), write_only=True, source='service'
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'client', 'service', 'service_id',
            'status', 'scheduled_date', 'message', 'location',
            'agreed_price', 'is_barter', 'barter_offer', 'created_at'
        ]


# --- 7. ReviewSerializer ---
class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    provider = UserSerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_provider=True), source='provider', write_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'provider', 'provider_id',
            'rating', 'comment', 'created_at'
        ]


# --- 8. TrustBadgeSerializer ---
class TrustBadgeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = TrustBadge
        fields = ['id', 'user', 'user_id', 'title', 'issuer', 'description', 'date_awarded']


# --- 9. MessageSerializer ---
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    recipient_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='recipient', write_only=True
    )

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'recipient', 'recipient_id',
            'text', 'audio_note', 'created_at'
        ]

# --- 10. PaymentTransactionSerializer ---
class PaymentTransactionSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    booking_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(), source='booking', write_only=True
    )

    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'booking', 'booking_id',
            'amount', 'status', 'created_at'
        ]

# --- 11. EscrowTransactionSerializer ---
class EscrowTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowTransaction
        fields = '__all__'


# --- 12. LocationSerializer ---
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
