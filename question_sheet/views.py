from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, \
    ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from question_sheet.models import QuestionSheet, Question
from question_sheet.serializer import QuestionSheetSerializer


class QuestionSheetViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = QuestionSheet.objects.all()
    serializer_class = QuestionSheetSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'id': serializer.data['id']}, status=status.HTTP_201_CREATED, headers=headers)


class QuestionSheetQuestions(GenericViewSet, ListModelMixin):
    def get_queryset(self):
        return Question.objects.filter(question_parent=ContentType.objects.get_for_model(QuestionSheet),
                                       question_parent__id=self.kwargs['pk'])

    serializer_class = QuestionSheetSerializer
    # serializer is not configured
