from django.contrib.auth import get_user_model
from django.db import models


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
    questions = models.ForeignKey('Question', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    has_progress_bar = models.BooleanField(default=False)
    is_one_question_each_page = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_KINDS = (
        'Range', 'Number', 'DropDownList', 'MultiChoice', 'Link', 'Email', 'File', 'Grading', 'Prioritization',
        'TextWithAnswer', 'Text', 'WelcomePage', 'ThanksPage', 'GroupQuestions'
    )
    kind = models.CharField(max_length=100, choices=QUESTION_KINDS)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, null=True, blank=True)
    is_required = models.BooleanField(default=False)
    has_question_num = models.BooleanField(default=False)

