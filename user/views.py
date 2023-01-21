from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user.models import Folder
from user.serializers import FolderSerializer
from .search import search_fields


class FolderViewSet(ModelViewSet):

    def get_queryset(self):
        self.search_fields = search_fields(self.request.query_params.get('filter'))

        return Folder.objects.prefetch_related('questionSheets').filter(owner=self.request.user)

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'questionSheets__name']
