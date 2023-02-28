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
    # TODO delete null=true
    uid = models.UUIDField(unique=True, null=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='fa')
    name = models.CharField(max_length=100, blank=True, default='Untitled')
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(auto_created=True)
    end_date = models.DateField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    has_progress_bar = models.BooleanField(default=False)
    is_one_question_each_page = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT, related_name='questionSheets', null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_required = models.BooleanField(default=False)
    has_question_num = models.BooleanField(default=False)
    media = models.FileField(upload_to='media/', null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'mp4'])])
    parent_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True,
                                    limit_choices_to={'model__in': ('questionsheet', 'groupquestions')})
    parent_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_type', 'parent_id')
    question_number = models.DecimalField(max_digits=5, decimal_places=1, default=0)

    def __str__(self):
        return self.title


class QuestionItem(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_items')
    field_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (
        'range', 'number', 'link', 'email', 'text', 'file', 'textwithanswer', 'drawerlist', 'grading', 'groupquestions',
        'prioritization', 'multichoice', 'welcomepage', 'thankspage')})
    field_object_id = models.PositiveIntegerField()
    field_object = GenericForeignKey('field_type', 'field_object_id')

    class Meta:
        unique_together = ('question', 'field_type', 'field_object_id')

    def __str__(self):
        return self.question.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer = models.JSONField(null=True, blank=True)
    file = models.FileField(upload_to='files/',
                            validators=[
                                FileExtensionValidator(
                                    allowed_extensions=['pdf', 'docx', 'jpg', 'jpeg', 'png'])], null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    answer_set = models.ForeignKey('AnswerSet', on_delete=models.SET_NULL, null=True, related_name='answers')

    def __str__(self):
        return self.question.id

    class Meta:
        unique_together = ('question', 'answer_set')


class AnswerSet(models.Model):
    question_sheet = models.ForeignKey(QuestionSheet, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_sheet.name
