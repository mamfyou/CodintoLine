from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from question_sheet.models.qsheet_models import QuestionSheet, QuestionItem
from question_sheet.serializers.qsheet_serializer import QuestionItemSerializer, QuestionSheetSerializer
from .permissions import *


class QuestionItemViewSet(ReadOnlyModelViewSet, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    def get_queryset(self):
        return QuestionItem.objects.select_related('question').all()

    serializer_class = QuestionItemSerializer

    def get_serializer_context(self):
        return {'request': self.request, 'pk': self.kwargs.get('questionSheet_pk')}


class QuestionSheetViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = QuestionSheet.objects.all()
    serializer_class = QuestionSheetSerializer
    permission_classes = [QuestionSheetPermission]
