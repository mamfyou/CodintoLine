from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models

from user.models import Folder


class QuestionSheet(models.Model):
    LANGUAGE_CHOICES = (
        ('ar', 'Arabic'),
        ('en', 'English'),
        ('fa', 'Persian'),
    )

    uid = models.UUIDField(unique=True, null=True, verbose_name='یو آیدی')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='fa', verbose_name='زبان')
    name = models.CharField(max_length=100, verbose_name='نام')
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name='صاحب پرسشنامه')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    start_date = models.DateField(auto_created=True, verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان')
    duration = models.DurationField(null=True, blank=True, verbose_name='مدت زمان پاسخگویی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    has_progress_bar = models.BooleanField(default=False, verbose_name='نمایش نوار پیشرفت')
    is_one_question_each_page = models.BooleanField(default=False, verbose_name='نمایش یک سوال در هر صفحه')
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT, related_name='questionSheetFolder', null=True,
                               blank=True, verbose_name='پوشه')

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='توضیحات')
    is_required = models.BooleanField(default=False, verbose_name='اجباری')
    has_question_num = models.BooleanField(default=False, verbose_name='نمایش شماره سوال')
    media = models.FileField(upload_to='media/', null=True, blank=True, verbose_name='عکس یا فیلم')
    parent_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True,
                                    limit_choices_to={'model__in': ('questionsheet', 'groupquestions')},
                                    related_query_name='questions', verbose_name='نوع والد')
    parent_id = models.PositiveIntegerField(verbose_name='شناسه والد')
    parent = GenericForeignKey('parent_type', 'parent_id')
    question_number = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name='شماره سوال')

    def __str__(self):
        return self.title


class QuestionItem(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_items',
                                 related_query_name='question_items', verbose_name='سوال')
    field_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (
        'range', 'number', 'link', 'email', 'text', 'file', 'textwithanswer', 'drawerlist', 'grading', 'groupquestions',
        'prioritization', 'multichoice', 'welcomepage', 'thankspage')}, related_query_name='question_itemss',
                                   verbose_name='نوع سوال')
    field_object_id = models.PositiveIntegerField(verbose_name='شناسه سوال')
    field_object = GenericForeignKey('field_type', 'field_object_id')

    class Meta:
        unique_together = ('question', 'field_type', 'field_object_id')

    def __str__(self):
        return self.question.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name='سوال')
    answer = models.JSONField(null=True, blank=True, verbose_name='پاسخ')
    file = models.FileField(upload_to='files/',
                            validators=[
                                FileExtensionValidator(
                                    allowed_extensions=['pdf', 'docx', 'jpg', 'jpeg', 'png'])], null=True, blank=True,
                            verbose_name='فایل')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    answer_set = models.ForeignKey('AnswerSet', on_delete=models.SET_NULL, null=True, related_name='answers',
                                   verbose_name='دسته جواب')

    def __str__(self):
        return self.question.id

    class Meta:
        unique_together = ('question', 'answer_set')


class AnswerSet(models.Model):
    question_sheet = models.ForeignKey(QuestionSheet, on_delete=models.CASCADE, verbose_name='پرسشنامه')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.question_sheet.name
