# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProfileViewSet, SkillViewSet, CategoryViewSet, ServiceViewSet,
    BookingViewSet, ReviewViewSet, TrustBadgeViewSet, MessageViewSet, PaymentTransactionViewSet,
    ProviderDashboardView, AdminDashboardView, CustomerDashboardView,
    LocationListView, LoginView, LogoutView, SignupView,
    VerifyEmailView, ResendVerificationView, AuthStatusView, check_auth
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'badges', TrustBadgeViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'transactions', PaymentTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Auth
    # urls.py
    # path("auth/status/", check_auth, name="check_auth"),
    path("auth/status/", AuthStatusView.as_view(), name="auth-status"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path("verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendVerificationView.as_view(), name="resend-verification"),
    # Dashboards
    path('dashboard/provider/', ProviderDashboardView.as_view(), name='provider-dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('dashboard/customer/', CustomerDashboardView.as_view(), name='customer-dashboard'),

    # Locations
    path("locations/", LocationListView.as_view(), name="location-list"),

    # DRF Login (for browsable API)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
