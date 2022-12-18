# from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from question_sheet.views import *

router = DefaultRouter()
router.register('', QuestionSheetViewSet, basename='question-sheet')

routers = NestedDefaultRouter(router, '', lookup='questionSheet')
routers.register('question', QuestionItemViewSet, basename='question')
urlpatterns = router.urls + routers.urls
