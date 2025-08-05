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
    PaymentTransactionSerializer, EscrowTransactionSerializer, LocationSerializer
)

# --- API Views ---

# --- 1. UserViewSet ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

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
# --- End of Views ---