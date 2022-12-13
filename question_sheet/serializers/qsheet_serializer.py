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
        fields = ['id', 'language', 'name', 'start_date', 'end_date', 'duration',
                  'has_progress_bar', 'is_one_question_each_page']

    def create(self, validated_data):
        return QuestionSheet.objects.create(user=self.context['request'].user, **validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'is_required', 'has_question_num', 'media', 'parent_type', 'parent_id',
                  'parent']

    def validate(self, attrs):
        if attrs.get('title') is None:
            raise serializers.ValidationError('متن سوال اجباری است!')
        elif attrs.get('title') == '':
            raise serializers.ValidationError('متن سوال اجباری است!')
        elif len(attrs.get('title')) < 5:
            raise serializers.ValidationError('متن سوال باید حداقل 5 کاراکتر باشد!')
        elif attrs.get('media').size > 2097152:
            raise serializers.ValidationError('حجم فایل باید کمتر از 20 مگابایت باشد!')
        elif attrs.get('media').content_type not in ['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml',
                                                     'image/webp', 'video/mp4', 'video/ogg', 'video/webm']:
            raise serializers.ValidationError('فرمت فایل ارسالی پشتیبانی نمی شود!')
        elif attrs.get('parent_type') is None:
            raise serializers.ValidationError('نوع والد سوال اجباری است!')
        return attrs


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

    def validate(self, data):
        if data.get('field_type') is None:
            raise serializers.ValidationError('نوع سوال اجباری است!')
        elif data.get('field_type') not in ContentType.objects.all():
            raise serializers.ValidationError('نوع سوال اشتباه است!')
        elif data.get('question') is None:
            raise serializers.ValidationError('سوال اجباری است!')
        elif data.get('field_object') is None:
            raise serializers.ValidationError('محتوای سوال اجباری است!')
        return data
