import datetime
import json
import uuid

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
        fields = ['id', 'uid', 'language', 'name', 'start_date', 'end_date', 'duration',
                  'has_progress_bar', 'is_one_question_each_page', 'folder']
        extra_kwargs = {
            'start_date': {'required': False},
            'language': {'required': False},
            'uid': {'read_only': True}
        }

    def create(self, validated_data):
        if validated_data.get('start_date') is None:
            return QuestionSheet.objects.create(owner=self.context['user'],
                                                start_date=datetime.date.today(), uid=uuid.uuid4(), **validated_data)
        return QuestionSheet.objects.create(owner=self.context['user'], uid=uuid.uuid4(), **validated_data)

    def validate(self, attrs):
        if attrs.get('folder') is None:
            raise serializers.ValidationError('پوشه نمیتواند خالی باشد!')
        elif attrs['folder'].owner != self.context['user']:
            raise serializers.ValidationError('شما نمیتوانید پوشه ای که متعلق به شما نیست را انتخاب کنید!')
        print(self.context['pk'])
        if self.context['pk2'] is not None:
            if attrs.get('name') is None or attrs.get('name') == "":
                raise serializers.ValidationError('نام اجباری است!')
        return attrs


class QuestionSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'options', 'description', 'is_required', 'has_question_num', 'media', 'parent_type',
                  'parent__type', 'parent_id', 'question_number']
        extra_kwargs = {
            'parent_type': {'write_only': True}
        }

    options = OptionsSerializer(many=True, required=False)
    parent__type = serializers.StringRelatedField(read_only=True, source='parent_type')

    def validate(self, attrs):
        if attrs.get('title') is None or attrs.get('title') == '':
            raise serializers.ValidationError('متن سوال اجباری است!')
        elif len(attrs.get('title')) < 5:
            raise serializers.ValidationError('متن سوال باید حداقل 5 کاراکتر باشد!')
        elif attrs.get('media') is not None:
            if attrs.get('media').size > 5242880:
                raise serializers.ValidationError('حجم فایل باید کمتر از 5 مگابایت باشد!')
            elif attrs.get('media').content_type not in ['image/jpeg', 'image/png', 'video/mp4', 'video/m4a']:
                raise serializers.ValidationError('فرمت فایل ارسالی پشتیبانی نمی شود! قابل قبول : png,jpeg,mp4,m4a')
        elif attrs.get('parent_type') is None:
            raise serializers.ValidationError('نوع والد سوال اجباری است!')
        return attrs


class QuestionItemSimpleSerializer(serializers.ModelSerializer):
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
        qsheet_obj = QuestionSheet.objects.get(id=self.context['pk'])
        print(qsheet_obj.uid)
        question_data = validated_data.pop('question')
        field_object_data = validated_data.pop('field_object')
        field_type_data = validated_data.pop('field_type')
        if question_data.get('options') is not None:
            options = question_data.pop('options')
        created_option = []
        the_class = SERIALIZER_DICT[field_type_data].Meta.model
        question = Question.objects.create(**question_data)
        if field_type_data == "ThanksPage":
            field_object = the_class.objects.create(short_url_uuid=str(qsheet_obj.uid), **field_object_data)
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
        qsheet = QuestionSheet.objects.get(id=self.context['pk'])
        if data.get('field_type') is None:
            raise serializers.ValidationError('نوع سوال اجباری است!')
        elif data.get('field_type') not in ['DrawerList', 'MultiChoice', 'Prioritization'] and \
                data.get('question').get('options') is not None:
            raise serializers.ValidationError('سوال انتخابی نمی تواند دارای گزینه باشد!')
        elif data.get('field_type') in ['DrawerList', 'MultiChoice', 'Prioritization'] and \
                data.get('question').get('options') is None:
            raise serializers.ValidationError('گزینه ها اجباری هستند!')
        elif data.get('field_type') == "ThanksPage":
            if ThanksPage.objects.filter(short_url_uuid=qsheet.uid).exists():
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


class QuestionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionItem
        fields = ['id', 'field_type', 'field_object', 'question', 'question_item']

    question_item = serializers.SerializerMethodField(method_name='get_child_questions')

    def get_child_questions(self, obj):
        group_type = ContentType.objects.get_for_model(GroupQuestions)
        if obj.field_type == group_type:
            children = QuestionItem.objects.filter(question__parent_type=group_type,
                                                   question__parent_id=obj.question.id)
            data = QuestionItemSimpleSerializer(children, many=True).data
            return data
        return "sdf"

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
        qsheet_obj = QuestionSheet.objects.get(id=self.context['pk'])
        print(qsheet_obj.uid)
        question_data = validated_data.pop('question')
        field_object_data = validated_data.pop('field_object')
        field_type_data = validated_data.pop('field_type')
        if question_data.get('options') is not None:
            options = question_data.pop('options')
        created_option = []
        the_class = SERIALIZER_DICT[field_type_data].Meta.model
        question = Question.objects.create(**question_data)
        if field_type_data == "ThanksPage":
            field_object = the_class.objects.create(short_url_uuid=str(qsheet_obj.uid), **field_object_data)
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
        qsheet = QuestionSheet.objects.get(id=self.context['pk'])
        if data.get('field_type') is None:
            raise serializers.ValidationError('نوع سوال اجباری است!')
        elif data.get('field_type') not in ['DrawerList', 'MultiChoice', 'Prioritization'] and \
                data.get('question').get('options') is not None:
            raise serializers.ValidationError('سوال انتخابی نمی تواند دارای گزینه باشد!')
        elif data.get('field_type') in ['DrawerList', 'MultiChoice', 'Prioritization'] and \
                data.get('question').get('options') is None:
            raise serializers.ValidationError('گزینه ها اجباری هستند!')
        elif data.get('field_type') == "ThanksPage":
            if ThanksPage.objects.filter(short_url_uuid=qsheet.uid).exists():
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


class GroupQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupQuestions
        fields = ['id', 'button_shape', 'button_text', 'is_random_order', 'question_item']

    question_items = QuestionItemSerializer(source='question_items.all', many=True)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer', 'file', 'answer_set']
        extra_kwargs = {
            'file': {'required': False},
            'answer_set': {'read_only': True}
        }

    def validate(self, attrs):
        answers_questions = []
        question_item_object = QuestionItem.objects.get(question_id=attrs['question'].id)
        if attrs.get('answer') is None and type(question_item_object.field_object) != File:
            raise serializers.ValidationError('پاسخ اجباری است!')
        elif attrs.get('question') is None:
            raise serializers.ValidationError('سوال اجباری است!')
        answers_questions.append(attrs.get('question'))
        file_flag = type(question_item_object.field_object) == File
        if file_flag is False and attrs.get('file') is not None:
            raise serializers.ValidationError('ارسال فایل مجاز نمی باشد!')
        elif type(question_item_object.field_object) in [Text, GroupQuestions, WelcomePage, ThanksPage]:
            raise serializers.ValidationError('این سوال نمی تواند پاسخ داده شود!')
        VALIDATORS_DICT[type(question_item_object.field_object)](attrs.get('answer'), question_item_object,
                                                                 attrs.get('file'), len(answers_questions))
        if len(answers_questions) != len(set(answers_questions)):
            raise serializers.ValidationError('لطفا برای هر سوال فقط یک جواب ثبت کنید!')
        return attrs


class AnswerSetSerializer(WritableNestedModelSerializer):
    class Meta:
        model = AnswerSet
        fields = ['id', 'question_sheet', 'answers']

    answers = AnswerSerializer(many=True, required=False)

    def validate(self, data):
        if data.get('answers') is None:
            raise serializers.ValidationError('پاسخ ها اجباری است!')
        elif data.get('question_sheet') is None:
            raise serializers.ValidationError('سوالنامه اجباری است!')
        elif data['question_sheet'].id != int(self.context['pk']):
            raise serializers.ValidationError('ایدی باید مطابق یو آر ال باشد')
        return data
