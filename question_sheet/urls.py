# from django.urls import path
from rest_framework.routers import DefaultRouter
# from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
#
from question_sheet.views import *
#
# router = DefaultRouter()
# router.register('', QuestionSheetViewSet, basename='question-sheet')
# nested = NestedDefaultRouter(router, '', lookup='question_sheet')
# nested.register('preview', QuestionSheetQuestions , basename='question')
# router.register('question', QuestionViewSet, basename='question')
#
# urlpatterns = router.urls

router = DefaultRouter()
router.register('question', QuestionItemViewSet, basename='question')
router.register('', QuestionSheetViewSet, basename='question-sheet')
urlpatterns = router.urls
