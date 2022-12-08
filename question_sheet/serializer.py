from django.contrib.auth import get_user_model
from drf_writable_nested.serializers import WritableNestedModelSerializer
from generic_relations.relations import GenericRelatedField
from generic_relations.serializers import GenericModelSerializer
from rest_framework import serializers

from question.models import TextWithAnswer, GroupQuestions, Range, Link, Text, Number, Email, File, DrawerList, Grading, \
    Prioritization, MultiChoice, WelcomePage, ThanksPage
from question.serializer import TxtWithAnsSerializer, RangeSerializer, LinkSerializer, TextSerializer, NumberSerializer, \
    EmailSerializer, FileSerializer, DrawerListSerializer, GradingSerializer, PrioritizationSerializer, \
    MultiChoiceSerializer, GroupQuestionSerializer, WelcomePageSerializer, ThanksPageSerializer
from question_sheet.models import Question, QuestionItem, QuestionSheet

User = get_user_model()

SERIALIZER_DICT = {
    'range': RangeSerializer,
    'number': NumberSerializer,
    'link': LinkSerializer,
    'email': EmailSerializer,
    'text': TextSerializer,
    'file': FileSerializer,
    'textwithanswer': TxtWithAnsSerializer,
    'drawerlist': DrawerListSerializer,
    'grading': GradingSerializer,
    'groupquestions': GroupQuestionSerializer,
    'prioritization': PrioritizationSerializer,
    'multichoice': MultiChoiceSerializer,
    'welcomepage': WelcomePageSerializer,
    'thankspage: ': ThanksPageSerializer,
}


class QuestionSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSheet
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionItemSerializer(WritableNestedModelSerializer):
    field_object = GenericRelatedField({
        TextWithAnswer: TxtWithAnsSerializer(),
        Range: RangeSerializer(),
        Link: LinkSerializer(),
        Text: TextSerializer(),
        Number: NumberSerializer(),
        Email: EmailSerializer(),
        File: FileSerializer(),
        DrawerList: DrawerListSerializer(),
        Grading: GradingSerializer(),
        Prioritization: PrioritizationSerializer(),
        MultiChoice: MultiChoiceSerializer(),
        GroupQuestions: GroupQuestionSerializer(),
        WelcomePage: WelcomePageSerializer(),
        ThanksPage: ThanksPageSerializer(),
    })
    question = QuestionSerializer()

    class Meta:
        model = QuestionItem
        fields = ['question', 'field_object', 'field_type']
