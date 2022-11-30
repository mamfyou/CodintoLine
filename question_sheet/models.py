from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class QuestionContentType(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('QuestionSheet', 'GroupQuestion')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class QuestionFields(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='question_fields',
                                     limit_choices_to={'model__in': (
                                         'Range', 'Number', 'DropDownList', 'MultiChoice', 'Link', 'Email', 'File',
                                         'Grading', 'Prioritization',
                                         'TextWithAnswer', 'Text', 'WelcomePage', 'ThanksPage', 'GroupQuestions')})

    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    unique_together = ('content_type', 'object_id')


class QuestionSheet(models.Model):
    LANGUAGE_CHOICES = (
        ('ar', 'Arabic'),
        ('en', 'English'),
        ('fa', 'Persian'),
    )
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    duration = models.DurationField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    has_progress_bar = models.BooleanField(default=False)
    is_one_question_each_page = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_KINDS = (
        ('rng', 'Range'), ('num', 'Number'), ('ddlist', 'DropDownList'), ('mulch', 'MultiChoice'), ('link', 'Link'),
        ('email', 'Email'), ('file', 'File'), ('grd', 'Grading'), ('prior', 'Prioritization'),
        ('txtwa', 'TextWithAnswer'), ('txt', 'Text'), ('wel', 'WelcomePage'), ('thanks', 'ThanksPage'),
        ('gq', 'GroupQuestions')
    )
    kind = models.CharField(max_length=100, choices=QUESTION_KINDS)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_required = models.BooleanField(default=False)
    has_question_num = models.BooleanField(default=False)
    question_parent = GenericRelation(QuestionContentType, related_query_name='question_parent')
    question_fields = GenericRelation(QuestionFields, related_query_name='question_fields')
    media = models.FileField(upload_to='media/', null=True, blank=True)
