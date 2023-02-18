from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from question_sheet.models.qsheet_models import QuestionSheet


class IsSuperUserOrOwnerOrIsActive(BasePermission):
    def has_permission(self, request, view):
        qsheet_obj = get_object_or_404(QuestionSheet, id=view.kwargs['questionSheet_pk'])
        if qsheet_obj.start_date is not None and qsheet_obj.end_date is not None:
            return request.user.is_superuser or \
                   qsheet_obj.owner == request.user or (
                           (qsheet_obj.start_date <= datetime.now().date() <= qsheet_obj.end_date) and
                           request.method in SAFE_METHODS)
        elif qsheet_obj.start_date is None:
            return request.user.is_superuser or \
                   qsheet_obj.owner == request.user or (
                           (datetime.now().date() <= qsheet_obj.end_date) and
                           request.method in SAFE_METHODS)
        elif qsheet_obj.end_date is None:
            return request.user.is_superuser or \
                   qsheet_obj.owner == request.user or (
                           (qsheet_obj.start_date <= datetime.now().date()) and
                           request.method in SAFE_METHODS)


class IsSuperUserOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        qsheet_obj = get_object_or_404(QuestionSheet, id=view.kwargs['questionSheet_pk'])
        if qsheet_obj.start_date is not None and qsheet_obj.end_date is not None:
            return request.user.is_superuser or \
                   qsheet_obj.owner == request.user or \
                   request.method in SAFE_METHODS


class IsSuperUserOrOwnerOrCreatePutOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.method in ['POST', 'OPTIONS', 'HEAD']:
            qsheet_obj = get_object_or_404(QuestionSheet, id=view.kwargs['questionSheet_pk'])
            return request.user == qsheet_obj.owner or request.user.is_superuser
        return True
