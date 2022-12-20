from rest_framework import status
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ModelViewSet

from question_sheet.models.qsheet_models import QuestionSheet, QuestionItem
from question_sheet.serializers.qsheet_serializer import QuestionItemSerializer, QuestionSheetSerializer
from .permissions import *


class QuestionItemViewSet(ReadOnlyModelViewSet, CreateModelMixin, DestroyModelMixin, GenericViewSet):
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
