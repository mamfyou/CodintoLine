import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class QuestionSheet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    LANGUAGE_CHOICES = (
        ('ar', 'Arabic'),
        ('en', 'English'),
        ('fa', 'Persian'),
    )
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    name = models.CharField(max_length=100, blank=True, default='Untitled')
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(auto_created=True)
    end_date = models.DateField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    has_progress_bar = models.BooleanField(default=False)
    is_one_question_each_page = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_required = models.BooleanField(default=False)
    has_question_num = models.BooleanField(default=False)
    media = models.FileField(upload_to='media/', null=True, blank=True)
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                    limit_choices_to={'model__in': ('questionsheet', 'groupquestions')})
    parent_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_type', 'parent_id')

    def __str__(self):
        return self.title


class QuestionItem(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    field_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (
        'range', 'number', 'link', 'email', 'text', 'file', 'textwithanswer', 'drawerlist', 'grading', 'groupquestions',
        'prioritization', 'multichoice', 'welcomepage', 'thankspage')})
    field_object_id = models.PositiveIntegerField()
    field_object = GenericForeignKey('field_type', 'field_object_id')

    class Meta:
        unique_together = ('question', 'field_type', 'field_object_id')

    def __str__(self):
        return self.question.title


# class Answer(models.Model):
