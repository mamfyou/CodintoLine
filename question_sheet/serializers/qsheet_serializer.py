from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from generic_relations.relations import GenericRelatedField

from question_sheet.models.qsheet_models import Question, QuestionItem, QuestionSheet
from question_sheet.serializers.question_serializer import *


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

    def get_serializer_for_instance(self, instance):
        for serializer in self.serializers.values():
            if isinstance(instance, serializer.Meta.model):
                return serializer
        raise serializers.ValidationError('Could not determine a valid serializer for instance %r.' % instance)


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
        fields = ['id', 'field_type', 'field_object', 'question']

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

    def create(self, validated_data):
        question_data = validated_data.pop('question')
        field_object_data = validated_data.pop('field_object')
        field_type_data = validated_data.pop('field_type').id
        the_class = ContentType.objects.get(id=field_type_data).model_class()
        question = Question.objects.create(**question_data)
        field_object = the_class.objects.create(**field_object_data)
        question_item = QuestionItem.objects.create(question=question, field_object=field_object, **validated_data)
        return question_item

    def validate(self, attrs):
        print(attrs)
        if attrs['question'].get('title') is None:
            raise serializers.ValidationError('متن سوال اجباری است!')
        elif attrs['question'].get('description') is None:
            raise serializers.ValidationError('توضیحات سوال اجباری است!')
        elif attrs['question'].get('parent_type') is None:
            raise serializers.ValidationError('نوع سوال اجباری است!')
        elif attrs['question'].get('parent_id') is None:
            raise serializers.ValidationError('شناسه سوال اجباری است!')
        elif attrs.get('field_type') is None:
            raise serializers.ValidationError('نوع سوال اجباری است!')
        elif attrs.get('field_object') is None:
            raise serializers.ValidationError('فیلد های اضافه سوال اجباری است!')
        return attrs
