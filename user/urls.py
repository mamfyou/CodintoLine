from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('folder', FolderViewSet, basename='folder')

urlpatterns = router.urls
