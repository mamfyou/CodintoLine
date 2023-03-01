from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from question_sheet.views import *

router = DefaultRouter()
router2 = DefaultRouter()
router.register('qsheet', QuestionSheetViewSet, basename='question-sheet')
router2.register('all', QuestionSheetAllViewSet, basename='question-sheet-all')

nested_router = NestedDefaultRouter(router, 'qsheet', lookup='questionSheet')
nested_router2 = NestedDefaultRouter(router2, 'all', lookup='questionSheetAll')

nested_router2.register('question', QuestionItemAllViewSet, basename='questions')
nested_router.register('answer', AnswerSetViewSet, basename='answer')
nested_router.register('question', QuestionItemViewSet, basename='question')
urlpatterns = router.urls + nested_router.urls + router2.urls + nested_router2.urls
