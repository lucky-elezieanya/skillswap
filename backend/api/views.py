import logging
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models import Count, Sum, Avg, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import redirect

from django.utils.encoding import force_str
from django.utils.http import  urlsafe_base64_decode

from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    User, Profile, Skill, Category, Service, Booking,
    Review, TrustBadge, Message, PaymentTransaction,
    EscrowTransaction, Location
)
from .serializers import (
    UserSerializer, ProfileSerializer, SkillSerializer,
    CategorySerializer, ServiceSerializer, BookingSerializer,
    ReviewSerializer, TrustBadgeSerializer, MessageSerializer,
    PaymentTransactionSerializer, EscrowTransactionSerializer,
    LocationSerializer, SignupSerializer
)
from .filters import ServiceFilter
from .utils.email import send_verification_email

logger = logging.getLogger(__name__)
User = get_user_model()

# --- API Views ---
# --- 1. UserViewSet ---
class AuthStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "is_authenticated": True,
            "user": {
                "id": request.user.id,
                "email": request.user.email,
                "username": request.user.username
            }
        })

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

class EscrowTransactionViewSet(viewsets.ModelViewSet):
    queryset = EscrowTransaction.objects.all()
    serializer_class = EscrowTransactionSerializer
    permission_classes = [IsAdminUser]

# --- 11. Dashboard Views ---
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

# --- 12. Admin Dashboard View ---
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

# --- 13. Customer Dashboard view ---
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

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the token from database
            request.user.auth_token.delete()
        except Exception:
            pass  # In case token was already deleted

        # Clear the cookie
        response = Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie("token")
        return response

# --- Signup and Email Verification Views ---
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
            # ✅ Redirect to frontend login page
            frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
            return redirect(f"{frontend_url}/login?verified=true")

        return Response(
            {"message": "Invalid or expired token."},
            status=status.HTTP_400_BAD_REQUEST
        )

class ResendVerificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.is_verified:
            return Response({"message": "User is already verified."}, status=400) 
        send_verification_email(user, request)
        return Response({"message": "Verification email resent successfully."})

# --- End of Views ---                                                                                                                                        h