from django.urls import path
from rest_framework.routers import DefaultRouter

from question.views import *

router = DefaultRouter()
router.register('txtwithans', TxtWithAnsViewSet, basename='text_with_answer')
router.register('thnxpage', ThanksPageViewSet, basename='thanks-page')

urlpatterns = router.urls
