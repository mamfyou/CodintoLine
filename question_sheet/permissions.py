from datetime import datetime

from rest_framework.permissions import BasePermission, SAFE_METHODS

from question_sheet.models.qsheet_models import QuestionSheet


class QuestionSheetPermission(BasePermission):
    def has_object_permission(self, obj: QuestionSheet, request, view):
        return request.user.is_superuser and (
                obj.end_date < datetime.now().date() or obj.start_date > datetime.now().date())
