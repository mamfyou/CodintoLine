from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Question


class TxtWithAnsViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Question.objects.filter(question_fields='text_with_answer')
