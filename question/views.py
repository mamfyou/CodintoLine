from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializer import *


class TxtWithAnsViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = TextWithAnswer.objects.all()
    serializer_class = TxtWithAnsSerializer


class ThanksPageViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = ThanksPage.objects.all()
    serializer_class = ThanksPageSerializer


class WelcomePageViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = WelcomePage.objects.all()
    serializer_class = WelcomePageSerializer


class GroupQuestionViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = GroupQuestions.objects.all()
    serializer_class = GroupQuestionSerializer


class MultiChoiceViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = MultiChoice.objects.all()
    serializer_class = MultiChoiceSerializer


class PrioritizationViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Prioritization.objects.all()
    serializer_class = PrioritizationSerializer


class GradingViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Grading.objects.all()
    serializer_class = GradingSerializer


class NumberViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Number.objects.all()
    serializer_class = NumberSerializer


class LinkViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class TextViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Text.objects.all()
    serializer_class = TextSerializer


class EmailViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class FileViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class DrawerListViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = DrawerList.objects.all()
    serializer_class = DrawerListSerializer


class RangeViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Range.objects.all()
    serializer_class = RangeSerializer
