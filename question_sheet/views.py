from rest_framework.viewsets import ModelViewSet

from question_sheet.models.qsheet_models import QuestionSheet, QuestionItem
from question_sheet.serializers.qsheet_serializer import QuestionItemSerializer, QuestionSheetSerializer


class QuestionItemViewSet(ModelViewSet):
    def get_queryset(self):
        return QuestionItem.objects.select_related('question').all()

    serializer_class = QuestionItemSerializer

    def get_serializer_context(self):
        return {'request': self.request, 'pk': self.kwargs.get('questionSheet_pk')}


class QuestionSheetViewSet(ModelViewSet):
    queryset = QuestionSheet.objects.all()
    serializer_class = QuestionSheetSerializer
