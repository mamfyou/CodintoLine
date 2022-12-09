from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from drf_writable_nested.serializers import WritableNestedModelSerializer
from generic_relations.relations import GenericRelatedField

from question_sheet.serializers.question_serializer import *
from question_sheet.models.qsheet_models import Question, QuestionItem, QuestionSheet

User = get_user_model()


# SERIALIZER_DICT = {
#     'range': RangeSerializer,
#     'number': NumberSerializer,
#     'link': LinkSerializer,
#     'email': EmailSerializer,
#     'text': TextSerializer,
#     'file': FileSerializer,
#     'textwithanswer': TxtWithAnsSerializer,
#     'drawerlist': DrawerListSerializer,
#     'grading': GradingSerializer,
#     'groupquestions': GroupQuestionSerializer,
#     'prioritization': PrioritizationSerializer,
#     'multichoice': MultiChoiceSerializer,
#     'welcomepage': WelcomePageSerializer,
#     'thankspage: ': ThanksPageSerializer,
# }


class GenericMamfRelatedField(GenericRelatedField):

    def to_internal_value(self, data):
        try:
            content_type = ContentType.objects.get(id=self.context['request'].data['field_type'])
            for serializer in self.serializers.values():
                if serializer.Meta.model == content_type:
                    return serializer.to_internal_value(data)
        except ImproperlyConfigured as e:
            raise serializers.ValidationError(e)


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


class QuestionItemSerializer(WritableNestedModelSerializer):
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
    })
    question = QuestionSerializer()

    class Meta:
        model = QuestionItem
        fields = ['question', 'field_object', 'field_type']
