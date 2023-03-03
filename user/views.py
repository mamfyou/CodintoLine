from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin

from user.models import Folder
from user.serializers import FolderSerializer, CodintoLineUserSerializer
from .search import search_fields
from .permission import IsSuperuserOrGetPutSelfOnly

class FolderViewSet(ModelViewSet):

    def get_queryset(self):
        self.search_fields = search_fields(self.request.query_params.get('filter'))

        return Folder.objects.prefetch_related('questionSheetFolder').filter(owner=self.request.user)

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'questionSheets__name']


class UserViewSet(ReadOnlyModelViewSet, UpdateModelMixin, GenericViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsSuperuserOrGetPutSelfOnly]
    serializer_class = CodintoLineUserSerializer

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
