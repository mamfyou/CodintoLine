from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from question_sheet.views import *

router = DefaultRouter()
router.register('', QuestionSheetViewSet, basename='question-sheet')
nested = NestedDefaultRouter(router, '', lookup='question_sheet')
nested.register('preview', QuestionSheetQuestions , basename='question')

urlpatterns = router.urls
