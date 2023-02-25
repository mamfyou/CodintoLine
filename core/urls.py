from rest_framework.routers import DefaultRouter

from core.views import LoginViewSet, SMSTokenCheckingViewSet, RefreshTokenViewSet

router = DefaultRouter()
router.register('login', LoginViewSet, basename='login')
router.register('token', SMSTokenCheckingViewSet, basename='token')
router.register('refresh-token', RefreshTokenViewSet, basename='refresh')

urlpatterns = router.urls
