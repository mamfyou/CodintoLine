from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializer import *


class TxtWithAnsViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = TextWithAnswer.objects.all()
    serializer_class = TxtWithAnsSerializer
    lookup_field = 'pk'


class ThanksPageViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = ThanksPage.objects.all()
    serializer_class = ThanksPageSerializer
    lookup_field = 'pk'


class WelcomePageViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = WelcomePage.objects.all()
    serializer_class = WelcomePageSerializer
    lookup_field = 'pk'


class GroupQuestionViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = GroupQuestions.objects.all()
    serializer_class = GroupQuestionSerializer
    lookup_field = 'pk'


class MultiChoiceViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = MultiChoice.objects.all()
    serializer_class = MultiChoiceSerializer
    lookup_field = 'pk'


class PrioritizationViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Prioritization.objects.all()
    serializer_class = PrioritizationSerializer
    lookup_field = 'pk'


class GradingViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Grading.objects.all()
    serializer_class = GradingSerializer
    lookup_field = 'pk'


class NumberViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Number.objects.all()
    serializer_class = NumberSerializer
    lookup_field = 'pk'


class LinkViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    lookup_field = 'pk'


class TextViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    lookup_field = 'pk'


class EmailViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    lookup_field = 'pk'


class FileViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'pk'


class DrawerListViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = DrawerList.objects.all()
    serializer_class = DrawerListSerializer
    lookup_field = 'pk'


class RangeViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Range.objects.all()
    serializer_class = RangeSerializer
    lookup_field = 'pk'
