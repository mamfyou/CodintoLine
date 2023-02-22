import datetime
import json

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from drf_writable_nested import WritableNestedModelSerializer
from generic_relations.relations import RenamedMethods
from generic_relations.serializers import GenericSerializerMixin

from question_sheet.models.qsheet_models import Question, QuestionItem, QuestionSheet, AnswerSet, Answer
from question_sheet.serializers.question_serializer import *
from question_sheet.validators import *

SERIALIZER_DICT = {
    'TextWithAnswer': TxtWithAnsSerializer(),
    'Range': RangeSerializer(),
    'Link': LinkSerializer(),
    'Text': TextSerializer(),
    'Number': NumberSerializer(),
    'Email': EmailSerializer(),
    'File': FileSerializer(),
    'DrawerList': DrawerListSerializer(),
    'Grading': GradingSerializer(),
    'Prioritization': PrioritizationSerializer(),
    'MultiChoice': MultiChoiceSerializer(),
    'GroupQuestions': GroupQuestionSerializer(),
    'WelcomePage': WelcomePageSerializer(),
    'ThanksPage': ThanksPageSerializer(),
}

VALIDATORS_DICT = {
    Range: range_validator,
    Email: email_validator,
    Link: link_validator,
    File: file_validator,
    Grading: grading_validator,
    Number: number_validator,
    Prioritization: prioritization_validator,
    DrawerList: drawerlist_validator,
    MultiChoice: multichoice_validator,
    TextWithAnswer: textwithanswer_validator,
}


class GenericMamfRelatedField(GenericSerializerMixin, serializers.JSONField, metaclass=RenamedMethods):

    def get_deserializer_for_data(self, value):
        serializer = SERIALIZER_DICT[self.context['request'].data['field_type']]
        try:
            serializer.to_internal_value(value)
        except Exception:
            raise ImproperlyConfigured('Invalid Data Format %r.' % value)
        return serializer

    def get_serializer_for_instance(self, instance):
        for serializer in self.serializers.values():
            if isinstance(instance, serializer.Meta.model):
                return serializer
        raise serializers.ValidationError('Could not determine a valid serializer for instance %r.' % instance)

    def to_internal_value(self, data):
        if type(data) is not dict:
            data = json.loads(data)
        try:
            serializer = self.get_deserializer_for_data(data)
        except ImproperlyConfigured as e:
            raise serializers.ValidationError(e)
        return serializer.to_internal_value(data)


class QuestionSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSheet
        fields = ['id', 'language', 'name', 'start_date', 'end_date', 'duration',
                  'has_progress_bar', 'is_one_question_each_page']
        extra_kwargs = {
            'start_date': {'required': False},
            'language': {'required': False}
        }

    def create(self, validated_data):
        if validated_data.get('start_date') is None:
            if validated_data.get('language') is None:
                return QuestionSheet.objects.create(owner=self.context['request'].user, language='fa',
                                                    start_date=datetime.date.today())
            return QuestionSheet.objects.create(owner=self.context['request'].user, start_date=datetime.date.today())
        return QuestionSheet.objects.create(owner=self.context['request'].user, **validated_data)


class QuestionSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'options', 'description', 'is_required', 'has_question_num', 'media', 'parent_type',
                  'parent_id', 'parent', 'question_number']

    options = OptionsSerializer(many=True, required=False)
    parent = QuestionSheetSerializer(read_only=True)

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

    def validate(self, attrs):
        if attrs.get('title') is None:
            raise serializers.ValidationError('متن سوال اجباری است!')
        elif attrs.get('title') == '':
            raise serializers.ValidationError('متن سوال اجباری است!')
        elif len(attrs.get('title')) < 5:
            raise serializers.ValidationError('متن سوال باید حداقل 5 کاراکتر باشد!')
        elif attrs.get('media') is not None:
            if attrs.get('media').size > 20971520:
                raise serializers.ValidationError('حجم فایل باید کمتر از 20 مگابایت باشد!')
            elif attrs.get('media').content_type not in ['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml',
                                                         'image/webp', 'video/mp4', 'video/ogg', 'video/webm']:
                raise serializers.ValidationError('فرمت فایل ارسالی پشتیبانی نمی شود!')
        elif attrs.get('parent_type') is None:
            raise serializers.ValidationError('نوع والد سوال اجباری است!')
        elif attrs.get('options') is not None:
            for option in attrs.get('options'):
                if option.get('name') is None:
                    raise serializers.ValidationError(f' متن گزینه {option} اجباری است! ')
                elif option.get('name') == '':
                    raise serializers.ValidationError(f'متن گزینه {option} اجباری است!')
                elif option.get('media') is not None:
                    if option.get('media').size > 2097152:
                        raise serializers.ValidationError('حجم فایل باید کمتر از 20 مگابایت باشد!')
                    elif option.get('media').content_type not in ['image/jpeg', 'image/png', 'image/gif',
                                                                  'image/svg+xml', 'image/webp', 'video/mp4',
                                                                  'video/ogg', 'video/webm']:
                        raise serializers.ValidationError('فرمت فایل ارسالی پشتیبانی نمی شود!')
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
    field_type = serializers.CharField()
    question = QuestionSerializer()

    def create(self, validated_data):
        options = []
        question_data = validated_data.pop('question')
        field_object_data = validated_data.pop('field_object')
        field_type_data = validated_data.pop('field_type')
        if question_data.get('options') is not None:
            options = question_data.pop('options')
        created_option = []
        the_class = SERIALIZER_DICT[field_type_data].Meta.model
        question = Question.objects.create(**question_data)
        if field_type_data == "ThanksPage":
            field_object = the_class.objects.create(short_url_uuid=self.context['pk'], **field_object_data)
        elif field_type_data in ["DrawerList", "Prioritization", "MultiChoice"]:
            for option_data in options:
                created_option.append(Option.objects.create(question=question, **option_data))
            question.options.set(created_option)
            field_object = the_class.objects.create(**field_object_data)
        else:
            field_object = the_class.objects.create(**field_object_data)
        question_item = QuestionItem.objects.create(question=question, field_object=field_object,
                                                    field_type=ContentType.objects.get_for_model(
                                                        SERIALIZER_DICT[field_type_data].Meta.model), **validated_data)
        return question_item

    def validate(self, data):
        if data.get('field_type') is None:
            raise serializers.ValidationError('نوع سوال اجباری است!')
        elif data.get('field_type') not in ['DrawerList', 'MultiChoice', 'Prioritization'] and \
                data.get('question').get('options') is not None:
            raise serializers.ValidationError('سوال انتخابی نمی تواند دارای گزینه باشد!')
        elif data.get('field_type') == "ThanksPage":
            if ThanksPage.objects.filter(short_url_uuid=self.context['pk']).exists():
                raise serializers.ValidationError('صفحه تشکر برای این سوالنامه قبلا ایجاد شده است!')
        elif data.get('field_type') == "WelcomePage":
            if QuestionItem.objects.filter(question__parent_id=data['question']['parent_id'],
                                           field_type=ContentType.objects.get_for_model(WelcomePage)).exists():
                raise serializers.ValidationError('صفحه خوش آمدگویی برای این سوالنامه قبلا ایجاد شده است!')
        elif data.get('field_type') not in SERIALIZER_DICT.keys():
            raise serializers.ValidationError('نوع سوال اشتباه است!')
        elif data.get('question') is None:
            raise serializers.ValidationError('سوال اجباری است!')
        elif data.get('field_type') in ['MultiChoice', 'DrawerList']:
            if len(data.get('question').get('options')) < data.get('field_object').get('min_selection'):
                raise serializers.ValidationError('حداقل تعیین شده بیشتر از تعداد گزینه ها است!')
        elif data.get('field_type') in ['MultiChoice', 'DrawerList']:
            if len(data.get('question').get('options')) > data.get('field_object').get('max_selection'):
                raise serializers.ValidationError('حداکثر تعیین شده بیشتر از تعداد گزینه ها است!')
        elif data.get('field_object') is None:
            raise serializers.ValidationError('محتوای سوال اجباری است!')
        SERIALIZER_DICT[data.get('field_type')].validate(data.get('field_object'))
        return data


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer', 'file', 'answer_set']
        extra_kwargs = {
            'file': {'required': False},
            'answer_set': {'read_only': True}
        }


class AnswerSetSerializer(WritableNestedModelSerializer):
    class Meta:
        model = AnswerSet
        fields = ['id', 'question_sheet', 'answers']

    answers = AnswerSerializer(many=True, required=False)

    def create(self, validated_data):
        answer_set = None
        if validated_data.get('answers') is not None:
            answers_data = validated_data.pop('answers')
            answers = []
            answer_set = AnswerSet.objects.create(**validated_data)
            for i in range(len(answers_data)):
                answers.append(
                    Answer.objects.create(answer=answers_data[i].get('answer'),
                                          answer_set=answer_set,
                                          question=answers_data[i]['question'],
                                          file=answers_data[i].get('file')))
            answer_set.answers.set(answers)
        return answer_set

    def validate(self, data):
        file_flag = False
        answers_questions = []
        if data.get('answers') is None:
            raise serializers.ValidationError('پاسخ ها اجباری است!')
        elif data.get('question_sheet') is None:
            raise serializers.ValidationError('سوالنامه اجباری است!')
        for i in data['answers']:
            object = QuestionItem.objects.get(question_id=i['question'].id)
            if i.get('answer') is None and type(object.field_object) != File:
                raise serializers.ValidationError('پاسخ اجباری است!')
            elif i.get('question') is None:
                raise serializers.ValidationError('سوال اجباری است!')
            answers_questions.append(i.get('question'))
            file_flag = type(object.field_object) == File
            if file_flag is False and i.get('file') is not None:
                raise serializers.ValidationError('ارسال فایل مجاز نمی باشد!')
            elif type(object.field_object) in [Text, GroupQuestions, WelcomePage, ThanksPage]:
                raise serializers.ValidationError('این سوال نمی تواند پاسخ داده شود!')
            VALIDATORS_DICT[type(object.field_object)](i.get('answer'), object, i.get('file'), len(answers_questions))
        if len(answers_questions) != len(set(answers_questions)):
            raise serializers.ValidationError('لطفا برای هر سوال فقط یک جواب ثبت کنید!')
        return data
