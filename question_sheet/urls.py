from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from question_sheet.views import *

router = DefaultRouter()
router2 = DefaultRouter()

router.register('qsheet', QuestionSheetViewSet, basename='question-sheet')

nested_router = NestedDefaultRouter(router, 'qsheet', lookup='questionSheet')
nested_router.register('answer', AnswerSetViewSet, basename='answer')
nested_router.register('question', QuestionItemViewSet, basename='questions')

# This is the url leading to all the question sheets and questions in read-only mode
# host/api/all/UUID/
router2.register('all', QuestionSheetAllViewSet, basename='question-sheet-all')

# the nested router for questions
# host/api/all/UUID/question/
nested_router2 = NestedDefaultRouter(router2, 'all', lookup='questionSheetAll')
nested_router2.register('question', QuestionItemAllViewSet, basename='questions')

urlpatterns = router.urls + nested_router.urls + router2.urls + nested_router2.urls
