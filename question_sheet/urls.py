# from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from question_sheet.views import *

router = DefaultRouter()
router.register('', QuestionSheetViewSet, basename='question-sheet')

nested_router = NestedDefaultRouter(router, '', lookup='questionSheet')
nested_router.register('answer', AnswerSetViewSet, basename='answer')
nested_router.register('question', QuestionItemViewSet, basename='question')
urlpatterns = router.urls + nested_router.urls
