import re

from rest_framework import serializers

from question_sheet.models.question_models import Option


def range_validator(value, instance, file, index):
    instance = instance.field_object
    for i in value:
        if i not in ['grade']:
            raise serializers.ValidationError(f'الگوی پاسخ ارسالی نامعتبر است در سوال {index} ام!')
    if type(value['grade']) != int:
        raise serializers.ValidationError(f'نمره باید عددی باشد در سوال {index} ام!')

    if value.get('grade') is None:
        raise serializers.ValidationError(f'نمره نمیتواند خالی باشد در سوال {index} ام!')
    elif instance.end_range_at is not None and int(value.get('grade')) > instance.end_range_at:
        raise serializers.ValidationError(f'عدد ارسالی باید کمتر از {instance.end_range_at} باشد در سوال {index} ام!')
    elif instance.start_range_at is not None and int(value.get('grade')) < instance.start_range_at:
        raise serializers.ValidationError(
            f'عدد ارسالی باید بیشتر از {instance.start_range_at} باشد در سوال {index} ام!')
    return value


def email_validator(value, instance, file, index):
    instance = instance.field_object
    for i in value:
        if i not in ['email']:
            raise serializers.ValidationError(f'الگوی پاسخ ارسالی نامعتبر است در سوال {index} ام!')
    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', str(value['email'])):
        raise serializers.ValidationError(f'ایمیل معتبر نیست در سوال {index} ام!')
    return value


def link_validator(value, instance, file, index):
    for i in value:
        if i not in ['link']:
            raise serializers.ValidationError(f'الگوی پاسخ ارسالی نامعتبر است در سوال {index} ام!')
    if re.search(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+$', value['link']) is None:
        raise serializers.ValidationError(f'لینک معتبر نمی باشد در سوال {index} ام!')
    return value


def file_validator(value, instance, file, index):
    instance = instance.field_object
    if file is None:
        raise serializers.ValidationError(f'فایل نمیتواند خالی باشد! در سوال {index} ام')
    if file.size > instance.max_size:
        raise serializers.ValidationError(
            f'حجم فایل بیشتر از حد مجاز است در سوال {index} ام! حد مجاز: ' + str(instance.max_size) + f' بایت')
    return value


def grading_validator(value, instance, file, index):
    instance = instance.field_object
    for i in value:
        if i not in ['grade']:
            raise serializers.ValidationError(f'الگوی پاسخ ارسالی نامعتبر است در سوال {index} ام!')
    if value.get('grade') is None:
        raise serializers.ValidationError(f'نمره نمیتواند خالی باشد در سوال {index} ام!')
    elif type(value['grade']) != int:
        raise serializers.ValidationError(f'نمره باید عددی باشد در سوال {index} ام!')
    elif instance.start_grade_at is not None and int(value.get('grade')) > instance.end_grade_at:
        raise serializers.ValidationError(
            f'عدد ارسالی باید کمتر از حداکثر {instance.end_grade_at} باشد در سوال {index} ام!')
    elif instance.end_grade_at is not None and int(value.get('grade')) < instance.start_grade_at:
        raise serializers.ValidationError(
            f'عدد ارسالی باید بیشتر از {instance.start_grade_at} باشد در سوال {index} ام!')
    return value


def number_validator(value, instance, file, index):
    instance = instance.field_object
    for i in value:
        if i not in ['number']:
            raise serializers.ValidationError(f'الگوی پاسخ ارسالی نامعتبر است!')
    if value.get('number') is None:
        raise serializers.ValidationError(f'عدد نمیتواند خالی باشد در سوال {index} ام!')
    elif type(value['number']) != int and type(value['number']) != float:
        raise serializers.ValidationError('عدد باید عددی باشد در سوال {index} ام!')
    elif instance.has_negative is False and value['number'] < 0:
        raise serializers.ValidationError(f'عدد ارسالی نمیتواند منفی باشد در سوال {index} ام!')
    elif instance.has_decimal is False and value['number'] % 1 != 0:
        raise serializers.ValidationError(f'عدد ارسالی نمیتواند اعشاری باشد در سوال {index} ام!')
    elif instance.min_num is not None and value['number'] < instance.min_num:
        raise serializers.ValidationError(
            f'عدد ارسالی نمیتواند کمتر از {instance.min_num} حد مجاز باشد در سوال {index} ام!')
    elif instance.max_num is not None and value['number'] > instance.max_num:
        raise serializers.ValidationError(
            f'عدد ارسالی نمیتواند بیشتر از حد مجاز {instance.max_num} باشد در سوال {index} ام!')
    return value


def prioritization_validator(value, instance, file, index):
    instance = instance.field_object
    for i in value:
        if i not in ['prioritization']:
            raise serializers.ValidationError(f'الگوی پاسخ ارسالی نامعتبر است در سوال {index} ام!')
    if value.get('prioritization') is None:
        raise serializers.ValidationError(f'عدد نمیتواند خالی باشد در سوال {index} ام!')
    elif type(value['prioritization']) != list:
        raise serializers.ValidationError(f'پاسخ باید به صورت آرایه باشد! در سوال {index} ام')
    return value


def drawerlist_validator(value, instance, file, index):
    options_id = [i.id for i in Option.objects.filter(question=instance.question)]
    for i in value:
        if i not in ['options']:
            raise serializers.ValidationError(f'الگوی پاسخ ارسالی نامعتبر است در سوال {index} ام!')
    if type(value['options']) != list:
        raise serializers.ValidationError(f'فرم ارسالی باید آرایه باشد در سوال {index} ام!')
    elif len(value['options']) > 1 and instance.field_object.is_multiple_choice is False:
        raise serializers.ValidationError(f'این سوال تنها یک گزینه را قبول میکند در سوال {index} ام!')
    elif len(
            value['options']) < instance.field_object.min_selection and instance.field_object.min_selection is not None:
        raise serializers.ValidationError(
            f'تعداد گزینه های ارسالی کمتر از حداقل {instance.field_object.min_selection} است در سوال {index} ام!')
    elif len(value['options']) < instance.field_object.max_selection and \
            instance.field_object.max_selection is not None:
        raise serializers.ValidationError(
            f'تعداد گزینه های ارسالی کمتر از حداقل {instance.field_object.max_selection} است در سوال {index} ام!')
    for i in value['options']:
        if i not in options_id:
            raise serializers.ValidationError(f'حداقل یکی از گزینه ارسالی معتبر نیست در سوال {index} ام!')
    return value


def multichoice_validator(value, instance, file, index):
    options_id = [i.id for i in Option.objects.filter(question=instance.question)]
    for i in value:
        if i not in ['options']:
            raise serializers.ValidationError(f'الگوی پاسخ ارسالی نامعتبر است در سوال {index} ام!')
    if type(value['options']) != list:
        raise serializers.ValidationError(f'فرم ارسالی باید آرایه باشد در سوال {index} ام!')
    elif len(
            value['options']) < instance.field_object.min_selection and instance.field_object.min_selection is not None:
        raise serializers.ValidationError(
            f'تعداد گزینه های ارسالی کمتر از حداقل {instance.field_object.min_selection} است در سوال {index} ام!')
    elif len(value['options']) < instance.field_object.max_selection and \
            instance.field_object.max_selection is not None:
        raise serializers.ValidationError(
            f'تعداد گزینه های ارسالی کمتر از حداقل {instance.field_object.max_selection} است در سوال {index} ام!')
    for i in value['options']:
        if i not in options_id:
            raise serializers.ValidationError(f'حداقل یکی از گزینه ارسالی معتبر نیست در سوال {index} ام!')
    return value


def textwithanswer_validator(value, instance, file, index):
    instance = instance.field_object
    validation_kind = instance.validation.get('kind')
    for i in value:
        if i not in ['answer_text']:
            raise serializers.ValidationError(f'الگوی پاسخ ارسالی نامعتبر است در سوال {index} ام!')
    if validation_kind is None:
        return value
    elif validation_kind == 'en_text':
        if not re.match(r'^[a-zA-Z0-9]*$', value['answer_text']):
            raise serializers.ValidationError(f'فقط از حروف انگلیسی و اعداد استفاده کنید در سوال {index} ام!')
    elif validation_kind == 'fa_text':
        if not re.match(r'^[۱-۹آ-ی0-9]*$', value['answer_text']):
            raise serializers.ValidationError(f'فقط از حروف فارسی و اعداد استفاده کنید در سوال {index} ام!')
    elif validation_kind in ['en_text', 'fa_text', 'regex']:
        if len(value['answer_text']) < instance.validation.get('min_length'):
            raise serializers.ValidationError(
                f'طول پاسخ باید حداقل {instance.validation.get("min_length")} باشد در سوال {index} ام!')
        elif len(value['answer_text']) > instance.validation.get('max_length'):
            raise serializers.ValidationError(
                f'طول پاسخ باید حداکثر {instance.validation.get("max_length")} باشد در سوال {index} ام!')
    elif validation_kind == 'number':
        if type(value['answer_text']) != int:
            raise serializers.ValidationError(f'پاسخ باید عددی باشد در سوال {index} ام!')
        elif instance.validation.get('min_length') is not None:
            if value['answer_text'] < instance.validation.get('min_length'):
                raise serializers.ValidationError(
                    f'پاسخ باید حداقل {instance.validation.get("min_length")} باشد در سوال {index} ام!')
        elif instance.validation.get('max_length') is not None:
            if value['answer_text'] > instance.validation.get('max_length'):
                raise serializers.ValidationError(
                    f'پاسخ باید حداکثر {instance.validation.get("max_length")} باشد در سوال {index} ام!')
    elif validation_kind == 'email':
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', value['answer_text']):
            raise serializers.ValidationError(f'پاسخ باید ایمیل باشد در سوال {index} ام!')
    elif validation_kind == 'cellphone':
        if not re.match(r'09[0-9]{9}', value['answer_text']):
            raise serializers.ValidationError(f'پاسخ باید شماره تلفن باشد در سوال {index} ام!')
    elif validation_kind == 'date':
        if not re.match(r'\d{4}-\d{2}-\d{2}', value['answer_text']):
            raise serializers.ValidationError(f'پاسخ باید تاریخ باشد در سوال {index} ام!')
    elif validation_kind == 'time':
        if not re.match(r'\d{2}:\d{2}', value['answer_text']):
            raise serializers.ValidationError(f'پاسخ باید زمان باشد در سوال {index} ام!')
    elif validation_kind == 'telephone':
        if not re.match(r'\d{2,4}-\d{7,8}', value['answer_text']):
            raise serializers.ValidationError(f'پاسخ باید تلفن باشد در سوال {index} ام!')
    elif validation_kind == 'ip':
        if not re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', value['answer_text']):
            raise serializers.ValidationError(f'پاسخ باید آی پی باشد در سوال {index} ام!')
    elif validation_kind == 'regex':
        if not re.match(instance.validation.get('regex'), value['answer_text']):
            raise serializers.ValidationError(f'پاسخ باید با الگوی مشخص شده مطابقت داشته باشد در سوال {index} ام!')
    return value
