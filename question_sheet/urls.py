from django.urls import path
from rest_framework.routers import DefaultRouter

from question_sheet.views import QuestionSheetViewSet

router = DefaultRouter()
router.register('qsheet', QuestionSheetViewSet, basename='question-sheet')

urlpatterns = router.urls