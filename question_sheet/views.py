import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from question_sheet.models.qsheet_models import QuestionItem, AnswerSet
from question_sheet.serializers.qsheet_serializer import QuestionItemSerializer, QuestionSheetSerializer, \
    AnswerSetSerializer
from user.serializers import QuestionSheetFolderSerializer
from .models.qsheet_models import QuestionSheet
from .permissions import *

class QuestionItemViewSet(ReadOnlyModelViewSet, UpdateModelMixin, CreateModelMixin, DestroyModelMixin):
    def get_queryset(self):
        qsheet = ContentType.objects.get_for_model(QuestionSheet)
        if self.kwargs.get('pk') is not None:
            return QuestionItem.objects.select_related('question').all()
        return QuestionItem.objects.select_related('question').filter(
            Q(question__parent_id=self.kwargs['questionSheet_pk']) & Q(question__parent_type=qsheet))

    serializer_class = QuestionItemSerializer
    permission_classes = [IsSuperUserOrOwnerOrIsActive, AccessToChildrenOnly]

    def get_serializer_context(self):
        return {'request': self.request, 'pk': self.kwargs.get('questionSheet_pk')}


class QuestionSheetViewSet(RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet, DestroyModelMixin):
    def get_queryset(self):
        return QuestionSheet.objects.filter(is_active=True, owner=self.request.user)

    serializer_class = QuestionSheetSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user': self.request.user, 'request': self.request, 'pk': self.kwargs.get('questionSheet_pk'),
                'pk2': self.kwargs.get('pk')}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Successfully Archived in database'})


class AnswerSetViewSet(ReadOnlyModelViewSet, CreateModelMixin):
    def get_queryset(self):
        return AnswerSet.objects.prefetch_related('answers').filter(
            question_sheet__id=self.kwargs.get('questionSheet_pk'))

    def get_serializer_context(self):
        return {'pk': self.kwargs.get('questionSheet_pk')}

    serializer_class = AnswerSetSerializer
    permission_classes = [IsSuperUserOrOwnerOrCreatePutOnly]


# These 2 Viewsets below are for accessing Question Sheets and Their Questions
# In a Safe Read-Only Mode
# The difference is anyone can access these views , and they only can read
class QuestionItemAllViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
        qsheet = ContentType.objects.get_for_model(QuestionSheet)
        qsheet_obj = QuestionSheet.objects.get(uid=self.kwargs['questionSheetAll_uid'])
        if self.kwargs.get('pk') is not None:
            return QuestionItem.objects.select_related('question').all()
        return QuestionItem.objects.select_related('question').filter(
            Q(question__parent_id=qsheet_obj.id) & Q(question__parent_type=qsheet))

    serializer_class = QuestionItemSerializer
    permission_classes = [IsSuperUserOrOwnerOrIsActiveAll, AccessToChildrenOnlyAll]

    def get_serializer_context(self):
        return {'request': self.request, 'pk': self.kwargs['questionSheetAll_uid']}


class QuestionSheetAllViewSet(RetrieveModelMixin, GenericViewSet):
    def get_queryset(self):
        return QuestionSheet.objects.filter(Q(is_active=True) & (
                Q(start_date__lte=datetime.datetime.today()) & Q(end_date__gte=datetime.datetime.today()) |
                Q(start_date__lte=datetime.datetime.today()) & Q(end_date=None)))

    serializer_class = QuestionSheetFolderSerializer
    lookup_field = 'uid'
    permission_classes = [IsSuperUser]
