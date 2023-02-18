from rest_framework import status
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from question_sheet.models.qsheet_models import QuestionItem, AnswerSet
from question_sheet.serializers.qsheet_serializer import QuestionItemSerializer, QuestionSheetSerializer, \
    AnswerSetSerializer
from .models.qsheet_models import QuestionSheet
from .permissions import IsSuperUserOrOwnerOrIsActive, IsSuperUserOrOwnerOrCreatePutOnly


class QuestionItemViewSet(ReadOnlyModelViewSet, CreateModelMixin, DestroyModelMixin):
    def get_queryset(self):
        return QuestionItem.objects.select_related('question').all()

    serializer_class = QuestionItemSerializer
    permission_classes = [IsSuperUserOrOwnerOrIsActive]

    def get_serializer_context(self):
        return {'request': self.request, 'pk': self.kwargs.get('questionSheet_pk')}


class QuestionSheetViewSet(ModelViewSet):
    def get_queryset(self):
        return QuestionSheet.objects.filter(is_active=True, owner=self.request.user)

    serializer_class = QuestionSheetSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Successfully Archived in database'})


class AnswerSetViewSet(ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin):
    def get_queryset(self):
        return AnswerSet.objects.prefetch_related('answers').filter(
            question_sheet__id=self.kwargs.get('questionSheet_pk'))

    serializer_class = AnswerSetSerializer
    permission_classes = [IsSuperUserOrOwnerOrCreatePutOnly]


