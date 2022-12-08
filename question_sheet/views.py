from rest_framework.viewsets import ModelViewSet

from question_sheet.models import QuestionSheet, QuestionItem
from question_sheet.serializer import QuestionItemSerializer, QuestionSheetSerializer


class QuestionItemViewSet(ModelViewSet):
    queryset = QuestionItem.objects.all()
    serializer_class = QuestionItemSerializer


class QuestionSheetViewSet(ModelViewSet):
    queryset = QuestionSheet.objects.all()
    serializer_class = QuestionSheetSerializer
