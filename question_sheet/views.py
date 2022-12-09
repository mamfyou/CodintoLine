from rest_framework.viewsets import ModelViewSet

from question_sheet.models.qsheet_models import QuestionSheet, QuestionItem
from question_sheet.serializers.qsheet_serializer import QuestionItemSerializer, QuestionSheetSerializer


class QuestionItemViewSet(ModelViewSet):
    queryset = QuestionItem.objects.all()
    serializer_class = QuestionItemSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class QuestionSheetViewSet(ModelViewSet):
    queryset = QuestionSheet.objects.all()
    serializer_class = QuestionSheetSerializer


