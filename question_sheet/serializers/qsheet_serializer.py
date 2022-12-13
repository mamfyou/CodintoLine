from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured

from drf_writable_nested.serializers import WritableNestedModelSerializer
from generic_relations.relations import GenericRelatedField

from question_sheet.models.qsheet_models import Question, QuestionItem, QuestionSheet
from question_sheet.serializers.question_serializer import *

# User = get_user_model()

SERIALIZER_DICT = {
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
}


class GenericMamfRelatedField(GenericRelatedField):

    def get_deserializer_for_data(self, value):
        serializerss = []
        for serializer in self.serializers.values():
            if ContentType.objects.get_for_model(serializer.Meta.model).id == \
                    self.context['request'].data['field_type']:
                try:
                    serializer.to_internal_value(value)
                    serializerss.append(serializer)
                except Exception:
                    pass
        l = len(serializerss)
        if l < 1:
            raise ImproperlyConfigured(
                'Could not determine a valid serializer for value %r.' % value)
        return serializerss[0]


class QuestionSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSheet
        fields = ['id', 'language', 'name', 'user', 'created', 'start_date', 'end_date', 'duration', 'is_active',
                  'has_progress_bar', 'is_one_question_each_page']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'is_required', 'has_question_num', 'media', 'parent_type', 'parent_id',
                  'parent']


class QuestionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionItem
        fields = ['id', 'field_type', 'field_object', 'field__object', 'question']

    field_object = GenericMamfRelatedField({
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
    }, write_only=True)

    question = QuestionSerializer()
    field__object = serializers.SerializerMethodField(method_name='get_field_object')

    def get_field_object(self, obj):
        for key, value in SERIALIZER_DICT.items():
            if isinstance(obj.field_object, key):
                return value.to_representation(obj.field_object)

    def create(self, validated_data):
        question_data = validated_data.pop('question')
        field_object_data = validated_data.pop('field_object')
        field_type_data = validated_data.pop('field_type').id
        the_class = ContentType.objects.get(id=field_type_data).model_class()
        question = Question.objects.create(**question_data)
        field_object = the_class.objects.create(**field_object_data)
        question_item = QuestionItem.objects.create(question=question, field_object=field_object, **validated_data)
        return question_item
