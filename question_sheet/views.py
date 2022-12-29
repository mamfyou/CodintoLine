from rest_framework import status
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ModelViewSet

from question_sheet.models.qsheet_models import QuestionItem, AnswerSet, Folder
from question_sheet.serializers.qsheet_serializer import QuestionItemSerializer, QuestionSheetSerializer, \
    AnswerSetSerializer, FolderSerializer
from .permissions import *


class QuestionItemViewSet(ReadOnlyModelViewSet, CreateModelMixin, DestroyModelMixin):
    def get_queryset(self):
        return QuestionItem.objects.select_related('question').all()

    serializer_class = QuestionItemSerializer
    permission_classes = [IsSuperUserOrOwnerOrIsActive]

    def get_serializer_context(self):
        return {'request': self.request, 'pk': self.kwargs.get('questionSheet_pk')}


class QuestionSheetViewSet(ModelViewSet):
    def get_queryset(self):
        return QuestionSheet.objects.filter(is_active=True)

    serializer_class = QuestionSheetSerializer
    permission_classes = [IsSuperuserOrOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Successfully Archived in database'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AnswerSetViewSet(ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin):
    def get_queryset(self):
        return AnswerSet.objects.prefetch_related('answers').filter(
            question_sheet__id=self.kwargs.get('questionSheet_pk'))

    serializer_class = AnswerSetSerializer


class FolderViewSet(ModelViewSet):
    def get_queryset(self):
        return Folder.objects.all()

    serializer_class = FolderSerializer
    permission_classes = [IsSuperuserOrOwner]
