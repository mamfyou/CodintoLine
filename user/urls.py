from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('profile', UserViewSet, basename='user')
router.register('folder', FolderViewSet, basename='folder')

urlpatterns = router.urls
