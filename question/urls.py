from django.urls import path
from rest_framework.routers import DefaultRouter

from question.views import *

router = DefaultRouter()
router.register('txtwithans', TxtWithAnsViewSet, basename='text_with_answer')
router.register('thnxpage', ThanksPageViewSet, basename='thanks-page')
router.register('welcomepage', WelcomePageViewSet, basename='welcome-page')
router.register('groupquestion', GroupQuestionViewSet, basename='group-question')
router.register('multichoice', MultiChoiceViewSet, basename='multi-choice')
router.register('prioritization', PrioritizationViewSet, basename='prioritization')
router.register('grading', GradingViewSet, basename='grading')
router.register('number', NumberViewSet, basename='number')
router.register('link', LinkViewSet, basename='link')
router.register('text', TextViewSet, basename='text')
router.register('email', EmailViewSet, basename='email')
router.register('file', FileViewSet, basename='file')
router.register('drawer', DrawerListViewSet, basename='drawer')
router.register('range', RangeViewSet, basename='range')

urlpatterns = router.urls
