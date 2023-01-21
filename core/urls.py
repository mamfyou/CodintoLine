from rest_framework.routers import DefaultRouter

from core.views import LoginViewSet, SMSTokenCheckingViewSet

router = DefaultRouter()
router.register('login', LoginViewSet, basename='login')
router.register('token', SMSTokenCheckingViewSet, basename='token')

urlpatterns = router.urls
