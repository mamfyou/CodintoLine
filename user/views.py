from rest_framework.viewsets import ModelViewSet

from user.models import Folder


# Create your views here.
class FolderViewSet(ModelViewSet):
    def get_queryset(self):
        return Folder.objects.all()

    # serializer_class = FolderSerializer
    # permission_classes = [IsSuperuserOrOwner]
