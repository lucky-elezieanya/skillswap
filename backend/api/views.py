from django.shortcuts import render
from rest_framework import viewsets, permissions, status,  generics, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.db.models import Q
from .models import (
    User, Profile, Skill, Category, Service, Booking,
    Review, TrustBadge, Message, PaymentTransaction, EscrowTransaction,  Location
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ServiceFilter

from .serializers import (
    UserSerializer, ProfileSerializer, SkillSerializer,
    CategorySerializer, ServiceSerializer, BookingSerializer,
    ReviewSerializer, TrustBadgeSerializer, MessageSerializer,
    PaymentTransactionSerializer, EscrowTransactionSerializer, LocationSerializer, SignupSerializer
)
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import EmailMultiAlternatives
from .utils.email import send_verification_email
import logging

logger = logging.getLogger(__name__)
User = get_user_model()
# --- API Views ---

# --- 1. UserViewSet ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':  # Allow signup
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
# --- 2. ProfileViewSet ---
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- 3. SkillViewSet ---
class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --- 4. CategoryViewSet ---
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# --- 5. ServiceViewSet ---

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

# --- 6. BookingViewSet ---
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status in ['pending', 'accepted']:
            booking.status = 'cancelled'
            booking.save()
            return Response({'status': 'Booking cancelled'})
        return Response({'error': 'Cannot cancel at this stage'}, status=400)

# --- 7. ReviewViewSet ---
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

# --- 8. TrustBadgeViewSet ---
class TrustBadgeViewSet(viewsets.ModelViewSet):
    queryset = TrustBadge.objects.all()
    serializer_class = TrustBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- 9. MessageViewSet ---
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# --- 10. PaymentTransactionViewSet ---
class PaymentTransactionViewSet(viewsets.ModelViewSet):
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def release(self, request, pk=None):
        transaction = self.get_object()
        if transaction.status == 'held':
            transaction.status = 'released'
            transaction.save()
            return Response({'status': 'Escrow released'})
        return Response({'error': 'Invalid state'}, status=400)

# --- Dashboard Views ---
class ProviderDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_provider:
            return Response({'error': 'Not a provider'}, status=403)

        year = request.query_params.get('year')
        month = request.query_params.get('month')
        filters = {}

        if year:
            filters['created_at__year'] = int(year)
        if month:
            filters['created_at__month'] = int(month)

        services = Service.objects.filter(provider=user)
        bookings = Booking.objects.filter(service__in=services, **filters)
        payments = PaymentTransaction.objects.filter(booking__in=bookings, status='released')
        reviews = Review.objects.filter(provider=user)

        # Chart data: bookings per month
        monthly_data = (
            bookings.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        data = {
            "total_services": services.count(),
            "total_bookings": bookings.count(),
            "total_earnings": payments.aggregate(total=Sum('amount'))['total'] or 0,
            "average_rating": reviews.aggregate(avg=Avg('rating'))['avg'] or 0,
            "booking_status_breakdown": bookings.values('status').annotate(count=Count('id')),
            "top_services": services.annotate(bookings=Count('booking')).order_by('-bookings')[:5].values('title', 'bookings'),
            "monthly_chart_data": list(monthly_data),
        }
        return Response(data)

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        total_providers = User.objects.filter(is_provider=True).count()
        total_services = Service.objects.count()
        total_bookings = Booking.objects.count()
        escrow_held = PaymentTransaction.objects.filter(status='held').aggregate(total=Sum('amount'))['total'] or 0
        escrow_released = PaymentTransaction.objects.filter(status='released').aggregate(total=Sum('amount'))['total'] or 0

        data = {
            "total_users": total_users,
            "total_providers": total_providers,
            "total_services": total_services,
            "total_bookings": total_bookings,
            "escrow_held": escrow_held,
            "escrow_released": escrow_released,
            "top_providers": User.objects.filter(is_provider=True)
                .annotate(num_services=Count('service'))
                .order_by('-num_services')[:5]
                .values('username', 'num_services')
        }
        return Response(data)

class CustomerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        bookings = Booking.objects.filter(customer=user)
        reviews = Review.objects.filter(customer=user)
        payments = PaymentTransaction.objects.filter(booking__in=bookings)

        data = {
            "total_bookings": bookings.count(),
            "total_reviews_given": reviews.count(),
            "total_spent": payments.aggregate(total=Sum('amount'))['total'] or 0,
            "recent_bookings": bookings.order_by('-created_at')[:5].values('service__title', 'status', 'created_at'),
            "favorites_count": user.favorites.count() if hasattr(user, 'favorites') else 0,
        }
        return Response(data)
    
class EscrowTransactionViewSet(viewsets.ModelViewSet):
    queryset = EscrowTransaction.objects.all()
    serializer_class = EscrowTransactionSerializer
    permission_classes = [IsAdminUser]

class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['city', 'state', 'country']
    filterset_fields = ['city', 'state', 'country']
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        identifier = request.data.get("identifier")  # username OR email
        password = request.data.get("password")
        if not identifier or not password:
            return Response({"detail": "Identifier and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        # If identifier is an email, get the username for authentication
        try:
            if "@" in identifier:
                user_obj = User.objects.filter(email__iexact=identifier).first()
                if user_obj:
                    identifier = user_obj.username
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            response = Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "is_provider": getattr(user, "is_provider", False),
            })
            # Set token as HTTP-only cookie
            response.set_cookie(
                "token",
                token.key,
                httponly=True,
                secure=False,  # Change to True in production with HTTPS
                samesite="Lax",
                max_age=60 * 60 * 24 * 7  # 1 week
            )
            return response

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# --- Signup and Email Verification Views ---
# class SignupView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         data = request.data
#         email = data.get('email')
#         username = data.get('username')
#         password = data.get('password')
#         phone = data.get('phone', '')
#         location = data.get('location', '')
#         is_provider = data.get('is_provider', False)

#         if not all([email, username, password]):
#             return Response({'detail': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             return Response({'detail': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(username=username).exists():
#             return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

#         # Create the user
#         user = User.objects.create(
#             username=username,
#             email=email,
#             password=make_password(password),
#             phone=phone,
#             location=location,
#             is_provider=is_provider,
#             is_verified=False,  # Wait for email verification
#         )

#         # Create authentication token
#         token = Token.objects.create(user=user)

#         # Generate email verification link
#         uid = urlsafe_base64_encode(force_bytes(user.pk))
#         email_token = default_token_generator.make_token(user)
#         verify_url = request.build_absolute_uri(
#             reverse("verify-email", kwargs={"uidb64": uid, "token": email_token})
#         )

#         # Try sending verification email, but don't break signup if it fails
#         try:
#             send_verification_email(user, request)
#         except Exception as e:
#             logger.error(f"Error sending verification email to {email}: {e}")
#             # Optional: attach the verify_url to response for manual testing
#             verify_url = request.build_absolute_uri(
#                 reverse("verify-email", kwargs={"uidb64": uid, "token": email_token})
#             )
#             return Response({
#                 "message": "Signup successful, but email could not be sent.",
#                 "verification_link": verify_url,  # helpful for local dev
#                 "token": token.key,
#                 "user_id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "is_provider": getattr(user, "is_provider", False),
#                 "is_verified": user.is_verified
#             }, status=status.HTTP_201_CREATED)

#         # Normal successful response
#         response = Response({
#             "message": "Signup successful. Verification email sent.",
#             "token": token.key,
#             "user_id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "is_provider": getattr(user, "is_provider", False),
#             "is_verified": user.is_verified
#         }, status=status.HTTP_201_CREATED)

#         # Set token as HTTP-only cookie for auto-login
#         response.set_cookie(
#             "token",
#             token.key,
#             httponly=True,
#             secure=False,  # Change to True in production
#             samesite="Lax",
#             max_age=60 * 60 * 24 * 1  # 1 day
#         )

#         return response

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone', '')
        location = data.get('location', '')
        is_provider = data.get('is_provider', False)

        if not all([email, username, password]):
            return Response({'detail': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'detail': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user but keep inactive until email is verified
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            phone=phone,
            location=location,
            is_provider=is_provider,
            is_verified=False,
            is_active=False,  # 🚨 Block login until verification
        )

        # Send verification email
        try:
            send_verification_email(user, request)
        except Exception as e:
            logger.error(f"Error sending verification email to {email}: {e}")
            return Response({
                "message": "Signup successful, but email could not be sent. Please contact support."
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Signup successful. Please check your email to verify your account."
        }, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"message": "Email verified successfully. You can now log in."})
        else:
            return Response({"message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_verified:
            return Response({"message": "User is already verified."}, status=400) 
        send_verification_email(user, request)
        return Response({"message": "Verification email resent successfully."})

# --- End of Views ---                                                                                                                                        