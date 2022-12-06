from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from question_sheet.models import QuestionFields
from .models import Question, TextWithAnswer
from .serializer import *
from django.contrib.contenttypes.models import ContentType


class TxtWithAnsViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = TextWithAnswer.objects.all()
    serializer_class = TxtWithAnsSerializer


class ThanksPageViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = ThanksPage.objects.all()
    serializer_class = ThanksPageSerializer
