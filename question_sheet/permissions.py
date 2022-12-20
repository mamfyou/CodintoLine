from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from question_sheet.models.qsheet_models import QuestionSheet


class IsSuperuserOrOwner(BasePermission):
    def has_object_permission(self, obj, request, view):
        Request = request.request
        return Request.user.is_superuser or \
               Request.user == view.owner


class IsSuperUserOrOwnerOrIsActive(BasePermission):
    def has_permission(self, request, view):
        # Request = request.user
        qsheet_obj = get_object_or_404(QuestionSheet, id=view.kwargs['questionSheet_pk'])
        return request.user.is_superuser or \
               qsheet_obj.owner == request.user or \
               ((qsheet_obj.start_date <= datetime.now().date() <= qsheet_obj.end_date) and
                request.method in SAFE_METHODS)
