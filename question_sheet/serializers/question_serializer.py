import re

from rest_framework import serializers

from question_sheet.models.question_models import TextWithAnswer, Range, Link, Text, Number, Email, File, DrawerList, Grading, Prioritization, \
    MultiChoice, GroupQuestions, WelcomePage, ThanksPage


class TxtWithAnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextWithAnswer
        fields = ['id', 'validation']

    def validate(self, attrs):
        is_number_regex = re.compile(r'^\d+$')
        validation = attrs.get('validation')
        if attrs.get('validation') is None:
            validation = attrs['validation']
            raise serializers.ValidationError('الگو اعتبار سنجی نمیتواند خالی باشد')
        elif validation.get('kind') is None:
            raise serializers.ValidationError('نوع الگو نمیتواند خالی باشد!')
        elif validation.get('kind') not in ['text', 'number', 'email', 'phone']:
            raise serializers.ValidationError('نوع الگو نامعتبر است!')
        elif validation.get('kind') == 'text' and attrs['validation'].get(
                'min_length') is not None and not re.Match(is_number_regex, attrs['validation'].get('min_length')):
            raise serializers.ValidationError('حداقل طول متن باید عدد باشد!')
        elif validation.get('kind') == 'text' and attrs['validation'].get(
                'max_length') is not None and not re.Match(is_number_regex, attrs['validation'].get('max_length')):
            raise serializers.ValidationError('حداکثر طول متن باید عدد باشد!')
        elif validation.get('kind') != 'text' and attrs['validation'].get('sample_pattern') is None:
            raise serializers.ValidationError('الگو نمونه نمیتواند خالی باشد!')
        elif validation.get('kind') != 'text' and attrs['validation'].get('evaluation_message') is None:
            raise serializers.ValidationError('پیام اعتبارسنجی نمیتواند خالی باشد!')

        return attrs


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
        return attrs


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'hint']


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'button_shape', 'button_text']


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
        if attrs.get('max_size') >= 100000000:
            raise serializers.ValidationError('حداکثر حجم فایل نمیتواند بیشتر از 100 مگابایت باشد!')
        return attrs


class DrawerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawerList
        fields = ['id', 'options', 'options_pic', 'min_selection', 'max_selection', 'is_random_order',
                  'is_alphabet_order', 'is_multiple_choice']

    is_multiple_choice = serializers.BooleanField(required=False)

    def validate(self, attrs):
        if attrs.get('min_selection') > attrs.get('max_selection'):
            raise serializers.ValidationError('حداقل انتخاب نمیتواند بیشتر از حداکثر انتخاب باشد!')
        elif attrs.get('options') is None and attrs.get('options_pic') is None:
            raise serializers.ValidationError('گزینه ها نمیتواند خالی باشد!')
        elif len(attrs['options']) + len(attrs['options_pic']) <= 1:
            raise serializers.ValidationError('تعداد گزینه ها باید بیشتر از یک باشد!')
        return attrs


class GradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grading
        fields = ['id', 'start_grade_at', 'end_grade_at', 'icon']

    def validate(self, attrs):
        if attrs.get('start_grade_at') > attrs.get('end_grade_at'):
            raise serializers.ValidationError('مقدار شروع بازه نمیتواند بزرگتر یا مساوی مقدار پایان بازه باشد!')
        elif attrs.get('icon') is not None and attrs.get('icon').size >= 3000000:
            raise serializers.ValidationError('حجم آیکون نمیتواند بیشتر از 3 مگابایت باشد!')
        elif attrs.get('icon') is not None and attrs.get('icon').content_type != 'PNG':
            raise serializers.ValidationError('فرمت آیکون باید PNG باشد!')
        return attrs


class PrioritizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioritization
        fields = ['id', 'options', 'options_pic', 'is_alphabetic_order', 'is_random_order']

    def validate(self, attrs):
        if attrs.get('options') is None and attrs.get('options_pic') is None:
            raise serializers.ValidationError('گزینه ها نمیتواند خالی باشد!')
        elif len(attrs['options']) + len(attrs['options_pic']) <= 1:
            raise serializers.ValidationError('تعداد گزینه ها باید بیشتر از یک باشد!')
        return attrs


class MultiChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoice
        fields = ['id', 'options', 'options_pic', 'min_selection', 'max_selection', 'is_extra_action', 'extra_actions',
                  'is_alphabetic_order', 'is_random_order', 'is_vertical_display', 'is_2x_picture', 'is_select_all']

    is_extra_action = serializers.BooleanField(required=False)

    def validate(self, attrs):
        if attrs.get('options') is None and attrs.get('options_pic') is None:
            raise serializers.ValidationError('گزینه ها نمیتواند خالی باشد!')
        elif attrs.get('min_selection') > attrs.get('max_selection'):
            raise serializers.ValidationError('حداقل انتخاب نمیتواند بیشتر از حداکثر انتخاب باشد!')
        elif attrs.get('extra_actions') is None and attrs.get('is_extra_action') is True:
            raise serializers.ValidationError('عملیات اضافی نمیتواند خالی باشد!')
        elif len(attrs['options']) + len(attrs['options_pic']) <= 1:
            raise serializers.ValidationError('تعداد گزینه ها باید بیشتر از یک باشد!')
        return attrs


class GroupQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupQuestions
        fields = ['id', 'button_shape', 'button_text', 'is_random_order']


class WelcomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelcomePage
        fields = ['id', 'button_shape', 'button_text']


class ThanksPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanksPage
        fields = ['id', 'link', 'has_social_link', 'has_eitaa', 'has_soroush', 'has_telegram', 'has_instagram',
                  'has_whatsapp']