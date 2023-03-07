import re

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from question_sheet.models.qsheet_models import Question
from question_sheet.models.question_models import TextWithAnswer, Range, Link, Text, Number, Email, File, DrawerList, \
    Grading, Prioritization, \
    MultiChoice, GroupQuestions, WelcomePage, ThanksPage, Option


class TxtWithAnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextWithAnswer
        fields = ['id', 'validation']

    def validate(self, attrs):
        is_number_regex = re.compile(r'^\d+$')
        validation = attrs.get('validation')
        if validation is None:
            raise serializers.ValidationError('ولیدیشن نمیتواند خالی باشد')
        elif validation.get('kind') is None:
            raise serializers.ValidationError('نوع الگو نمیتواند خالی باشد!')
        elif validation.get('kind') not in ['text', 'fa_text', 'en_text', 'number', 'cellphone', 'miladi_date',
                                            'shamsi_date', 'telephone']:
            raise serializers.ValidationError('نوع الگو نامعتبر است!')
        elif validation.get('kind') in ['en_text', 'fa_text'] and attrs['validation'].get(
                'min_length') is not None and not re.fullmatch(is_number_regex,
                                                               str(attrs['validation'].get('min_length'))):
            raise serializers.ValidationError('حداقل طول متن باید عدد باشد!')
        elif validation.get('kind') in ['en_text', 'fa_text'] and attrs['validation'].get(
                'max_length') is not None and not re.fullmatch(is_number_regex,
                                                               str(attrs['validation'].get('max_length'))):
            raise serializers.ValidationError('حداکثر طول متن باید عدد باشد!')
        elif validation.get('kind') in ['en_text', 'fa_text'] and validation.get('min_length') is not None:
            if validation.get(
                    'max_length') and validation.get('min_length') >= validation.get('max_length'):
                raise serializers.ValidationError('حداقل طول متن باید کمتر از حداکثر طول متن باشد!')
        elif validation.get('kind') not in ['en_text', 'fa_text'] and attrs['validation'].get('sample_pattern') is None:
            raise serializers.ValidationError('الگو نمونه نمیتواند خالی باشد!')
        elif validation.get('kind') not in ['en_text', 'fa_text'] and attrs['validation'].get(
                'evaluation_message') is None:
            raise serializers.ValidationError('پیام اعتبارسنجی نمیتواند خالی باشد!')


class RangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Range
        fields = ['id', 'start_range_at', 'end_range_at', 'first_tag', 'mid_tag', 'end_tag', 'has_zero']

    def validate(self, attrs):
        is_number_regex = re.compile(r'^\d+$')
        if attrs.get('start_range_at') is None:
            raise serializers.ValidationError('مقدار شروع بازه نمیتواند خالی باشد!')
        elif attrs.get('end_range_at') is None:
            raise serializers.ValidationError('مقدار پایان بازه نمیتواند خالی باشد!')
        elif attrs.get('start_range_at') and not re.fullmatch(is_number_regex, str(attrs.get('start_range_at'))):
            raise serializers.ValidationError('مقدار شروع بازه باید عدد باشد!')
        elif attrs.get('end_range_at') and not re.fullmatch(is_number_regex, str(attrs.get('end_range_at'))):
            raise serializers.ValidationError('مقدار پایان بازه باید عدد باشد!')
        return attrs


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'hint']


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'button_shape', 'button_text']

    def validate(self, attrs):
        if attrs.get('button_text') is not None and len(attrs.get('button_text')) > 50:
            raise serializers.ValidationError('متن دکمه نمیتواند بیشتر از 50 کاراکتر باشد!')
        elif attrs.get('button_shape') not in ['1', '2', '3', '4', '5', '6']:
            raise serializers.ValidationError('شکل دکمه نامعتبر است!')
        return attrs


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['id', 'min_num', 'max_num', 'has_decimal', 'has_negative']

    def validate(self, attrs):
        if attrs.get('min_num') > attrs.get('max_num'):
            raise serializers.ValidationError('حداقل مقدار نمیتواند بیشتر از حداکثر مقدار باشد!')
        return attrs


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'hint']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'max_size']

    def validate(self, attrs):
        if attrs.get('max_size') >= 10485760:
            raise serializers.ValidationError('حداکثر حجم فایل نمیتواند بیشتر از 10 مگابایت باشد!')
        return attrs


class DrawerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawerList
        fields = ['id', 'min_selection', 'max_selection', 'is_random_order',
                  'is_alphabetic_order']

    def validate(self, attrs):
        if attrs.get('min_selection') is None or attrs.get('max_selection') is None:
            raise serializers.ValidationError('حداقل و حداکثر انتخاب نمیتواند خالی باشد!')
        elif attrs.get('min_selection') > attrs.get('max_selection'):
            raise serializers.ValidationError('حداقل انتخاب نمیتواند بیشتر از حداکثر انتخاب باشد!')
        return attrs


class GradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grading
        fields = ['id', 'default_icon', 'end_grade_at', 'icon']

    def validate(self, attrs):
        if attrs.get('default_icon') is None and attrs.get('icon') is None:
            raise serializers.ValidationError('آیکون پیشفرض و آیکون نمیتواند هردو خالی باشد!')
        elif attrs.get('icon') is not None and attrs.get('icon').size >= 1048576:
            raise serializers.ValidationError('حجم آیکون نمیتواند بیشتر از 1 مگابایت باشد!')
        elif attrs.get('icon') is not None and attrs.get('icon').content_type not in ['image/png', 'image/svg']:
            raise serializers.ValidationError('فرمت آیکون باید PNG/SVG باشد!')
        return attrs


class PrioritizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioritization
        fields = ['id', 'is_alphabetic_order', 'is_random_order']


class MultiChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoice
        fields = ['id', 'min_selection', 'max_selection', 'is_extra_action', 'extra_actions',
                  'is_alphabetic_order', 'is_random_order', 'is_vertical_display', 'is_2x_picture', 'is_select_all']

    is_extra_action = serializers.BooleanField(required=False)

    def validate(self, attrs):
        if attrs.get('min_selection') is None or attrs.get('max_selection') is None:
            raise serializers.ValidationError('حداقل و حداکثر انتخاب نمیتواند خالی باشد!')
        elif attrs.get('min_selection') > attrs.get('max_selection'):
            raise serializers.ValidationError('حداقل انتخاب نمیتواند بیشتر از حداکثر انتخاب باشد!')
        return attrs


class GroupQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupQuestions
        fields = ['id', 'button_shape', 'button_text', 'is_random_order']


class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'name', 'order', 'picture']

    def validate(self, attrs):
        if attrs.get('name') is None:
            raise serializers.ValidationError(f' متن گزینه  اجباری است! ')
        elif attrs.get('name') == '':
            raise serializers.ValidationError(f'متن گزینه اجباری است!')
        elif attrs.get('media') is not None:
            if attrs.get('media').size > 5242880:
                raise serializers.ValidationError('حجم فایل باید کمتر از 5 مگابایت باشد!')
            elif attrs.get('media').content_type not in ['image/jpeg', 'image/png']:
                raise serializers.ValidationError('فرمت فایل ارسالی پشتیبانی نمی شود! قابل قبول : png, jpeg')
        return attrs

class WelcomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomePage
        fields = ['id', 'button_shape', 'button_text']

    def validate(self, attrs):
        if attrs.get('button_text') is not None and len(attrs.get('button_text')) > 50:
            raise serializers.ValidationError('متن دکمه نمیتواند بیشتر از 50 کاراکتر باشد!')
        elif attrs.get('button_shape') not in ['1', '2', '3', '4', '5', '6']:
            raise serializers.ValidationError('شکل دکمه نامعتبر است!')
        return attrs


class ThanksPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanksPage
        fields = ['id', 'short_url_uuid', 'has_social_link', 'has_eitaa', 'has_soroush', 'has_telegram',
                  'has_instagram', 'has_whatsapp']
        read_only_fields = ['short_url_uuid']



