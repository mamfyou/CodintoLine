import re

from rest_framework import serializers

from question_sheet.models.question_models import Option


def range_validator(value, instance, file):
    instance = instance.field_object
    for i in value:
        if i not in ['grade']:
            raise serializers.ValidationError('الگوی پاسخ ارسالی نامعتبر است!')
    if type(value['grade']) != int:
        raise serializers.ValidationError('نمره باید عددی باشد!')

    if value.get('grade') is None:
        raise serializers.ValidationError('نمره نمیتواند خالی باشد!')
    elif instance.end_range_at is not None and int(value.get('grade')) > instance.end_range_at:
        raise serializers.ValidationError(f'عدد ارسالی باید کمتر از {instance.end_range_at} باشد!')
    elif instance.start_range_at is not None and int(value.get('grade')) < instance.start_range_at:
        raise serializers.ValidationError(f'عدد ارسالی باید بیشتر از {instance.start_range_at} باشد!')
    return value


def email_validator(value, instance, file):
    instance = instance.field_object
    for i in value:
        if i not in ['email']:
            raise serializers.ValidationError('الگوی پاسخ ارسالی نامعتبر است!')
    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', str(value['email'])):
        raise serializers.ValidationError('ایمیل معتبر نیست!')
    return value


def link_validator(value, instance, file):
    for i in value:
        if i not in ['link']:
            raise serializers.ValidationError('الگوی پاسخ ارسالی نامعتبر است!')
    if re.search(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+$', value['link']) is None:
        raise serializers.ValidationError('لینک معتبر نمی باشد!')
    return value


def file_validator(value, instance, file):
    instance = instance.field_object
    if file is None:
        raise serializers.ValidationError('فایل نمیتواند خالی باشد!')
    if file.size > instance.max_size:
        raise serializers.ValidationError('حجم فایل بیشتر از حد مجاز است! حد مجاز: ' + str(instance.max_size) + ' بایت')
    if file.content_type not in ['application/pdf', 'application/msword',
                                 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                 'image/jpeg', 'image/png', 'image/gif', 'audio/mpeg', 'video/mp4']:
        raise serializers.ValidationError('نوع فایل مجاز نیست!')
    return value


def grading_validator(value, instance, file):
    instance = instance.field_object
    for i in value:
        if i not in ['grade']:
            raise serializers.ValidationError('الگوی پاسخ ارسالی نامعتبر است!')
    if value.get('grade') is None:
        raise serializers.ValidationError('نمره نمیتواند خالی باشد!')
    elif type(value['grade']) != int:
        raise serializers.ValidationError('نمره باید عددی باشد!')
    elif instance.start_grade_at is not None and int(value.get('grade')) > instance.end_grade_at:
        raise serializers.ValidationError(f'عدد ارسالی باید کمتر از حداکثر {instance.end_grade_at} باشد!')
    elif instance.end_grade_at is not None and int(value.get('grade')) < instance.start_grade_at:
        raise serializers.ValidationError(f'عدد ارسالی باید بیشتر از {instance.start_grade_at} باشد!')
    return value


def number_validator(value, instance, file):
    instance = instance.field_object
    for i in value:
        if i not in ['number']:
            raise serializers.ValidationError('الگوی پاسخ ارسالی نامعتبر است!')
    if value.get('number') is None:
        raise serializers.ValidationError('عدد نمیتواند خالی باشد!')
    elif type(value['number']) != int and type(value['number']) != float:
        raise serializers.ValidationError('عدد باید عددی باشد!')
    elif instance.has_negative is False and value['number'] < 0:
        raise serializers.ValidationError('عدد ارسالی نمیتواند منفی باشد!')
    elif instance.has_decimal is False and value['number'] % 1 != 0:
        raise serializers.ValidationError('عدد ارسالی نمیتواند اعشاری باشد!')
    elif instance.min_num is not None and value['number'] < instance.min_num:
        raise serializers.ValidationError(f'عدد ارسالی نمیتواند کمتر از {instance.min_num} حد مجاز باشد!')
    elif instance.max_num is not None and value['number'] > instance.max_num:
        raise serializers.ValidationError(f'عدد ارسالی نمیتواند بیشتر از حد مجاز {instance.max_num} باشد!')
    return value


def prioritization_validator(value, instance, file):
    instance = instance.field_object
    for i in value:
        if i not in ['prioritization']:
            raise serializers.ValidationError('الگوی پاسخ ارسالی نامعتبر است!')
    if value.get('prioritization') is None:
        raise serializers.ValidationError('عدد نمیتواند خالی باشد!')
    elif type(value['prioritization']) != list:
        raise serializers.ValidationError('پاسخ باید به صورت آرایه باشد!')
    return value


def drawerlist_validator(value, instance, file):
    # todo: add more validators
    options_id = [i.id for i in Option.objects.filter(question=instance.question)]
    for i in value:
        if i not in ['options']:
            raise serializers.ValidationError('الگوی پاسخ ارسالی نامعتبر است!')
    if type(value['options']) != list:
        raise serializers.ValidationError('فرم ارسالی باید آرایه باشد!')
    elif len(value['options']) > 1 and instance.field_object.is_multiple_choice is False:
        raise serializers.ValidationError('این سوال تنها یک گزینه را قبول میکند!')
    elif len(
            value['options']) < instance.field_object.min_selection and instance.field_object.min_selection is not None:
        raise serializers.ValidationError(
            f'تعداد گزینه های ارسالی کمتر از حداقل {instance.field_object.min_selection} است!')
    elif len(value['options']) < instance.field_object.max_selection and \
            instance.field_object.max_selection is not None:
        raise serializers.ValidationError(
            f'تعداد گزینه های ارسالی کمتر از حداقل {instance.field_object.max_selection} است!')
    for i in value['options']:
        if i not in options_id:
            raise serializers.ValidationError('حداقل یکی از گزینه ارسالی معتبر نیست!')
    return value


def multichoice_validator(value, instance, file):
    options_id = [i.id for i in Option.objects.filter(question=instance.question)]
    for i in value:
        if i not in ['options']:
            raise serializers.ValidationError('الگوی پاسخ ارسالی نامعتبر است!')
    if type(value['options']) != list:
        raise serializers.ValidationError('فرم ارسالی باید آرایه باشد!')
    elif len(
            value['options']) < instance.field_object.min_selection and instance.field_object.min_selection is not None:
        raise serializers.ValidationError(
            f'تعداد گزینه های ارسالی کمتر از حداقل {instance.field_object.min_selection} است!')
    elif len(value['options']) < instance.field_object.max_selection and \
            instance.field_object.max_selection is not None:
        raise serializers.ValidationError(
            f'تعداد گزینه های ارسالی کمتر از حداقل {instance.field_object.max_selection} است!')
    for i in value['options']:
        if i not in options_id:
            raise serializers.ValidationError('حداقل یکی از گزینه ارسالی معتبر نیست!')
    return value


def textwithanswer_validator(value, instance, file):
    instance = instance.field_object
    validation_kind = instance.validation.get('kind')
    for i in value:
        if i not in ['answer_text']:
            raise serializers.ValidationError('الگوی پاسخ ارسالی نامعتبر است!')
    if validation_kind is None:
        return value
    elif validation_kind == 'text':
        if len(value['answer_text']) < instance.validation.get('min_length'):
            raise serializers.ValidationError(
                f'طول پاسخ باید حداقل {instance.validation.get("min_length")} باشد!')
        elif len(value['answer_text']) > instance.validation.get('max_length'):
            raise serializers.ValidationError(
                f'طول پاسخ باید حداکثر {instance.validation.get("max_length")} باشد!')
    elif validation_kind == 'number':
        if type(value['answer_text']) != int:
            raise serializers.ValidationError('پاسخ باید عددی باشد!')
    elif validation_kind == 'email':
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', value['answer_text']):
            raise serializers.ValidationError('پاسخ باید ایمیل باشد!')
    elif validation_kind == 'cellphone':
        if not re.match(r'09[0-9]{9}', value['answer_text']):
            raise serializers.ValidationError('پاسخ باید شماره تلفن باشد!')
    elif validation_kind == 'date':
        if not re.match(r'\d{4}-\d{2}-\d{2}', value['answer_text']):
            raise serializers.ValidationError('پاسخ باید تاریخ باشد!')
    elif validation_kind == 'time':
        if not re.match(r'\d{2}:\d{2}', value['answer_text']):
            raise serializers.ValidationError('پاسخ باید زمان باشد!')
    elif validation_kind == 'telephone':
        if not re.match(r'\d{2,4}-\d{7,8}', value['answer_text']):
            raise serializers.ValidationError('پاسخ باید تلفن باشد!')
    elif validation_kind == 'ip':
        if not re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', value['answer_text']):
            raise serializers.ValidationError('پاسخ باید آی پی باشد!')
    elif validation_kind == 'regex':
        if not re.match(instance.validation.get('regex'), value['answer_text']):
            raise serializers.ValidationError('پاسخ باید با الگوی مشخص شده مطابقت داشته باشد!')
    return value

