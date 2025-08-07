# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import (
    ProviderDashboardView, AdminDashboardView, CustomerDashboardView,
    LocationListView, LoginView, SignupView, VerifyEmailView, ResendVerificationView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register('profiles', ProfileViewSet)
router.register('skills', SkillViewSet)
router.register('categories', CategoryViewSet)
router.register('services', ServiceViewSet)
router.register('bookings', BookingViewSet)
router.register('reviews', ReviewViewSet)
router.register('badges', TrustBadgeViewSet)
router.register('messages', MessageViewSet)
router.register('transactions', PaymentTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),  # ✅ Login 
    path("api/signup/", SignupView.as_view(), name="signup"),
    path("api/verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("api/resend-verification/", ResendVerificationView.as_view(), name="resend-verification"),

    path("api/verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),
    path('dashboard/provider/', ProviderDashboardView.as_view(), name='provider-dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('dashboard/customer/', CustomerDashboardView.as_view(), name='customer-dashboard'),
    path("locations/", LocationListView.as_view(), name="location-list"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
