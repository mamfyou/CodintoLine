from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.db import models

from question_sheet.models import Question, QuestionFields


# Create your models here.
class Range(models.Model):
    start_range_at = models.PositiveIntegerField()
    end_range_at = models.PositiveIntegerField()
    first_tag = models.CharField(max_length=50)
    mid_tag = models.CharField(max_length=50)
    end_tag = models.CharField(max_length=50)
    has_zero = models.BooleanField(default=False)
    question = GenericRelation(QuestionFields, related_query_name='range')


class Number(models.Model):
    min_num = models.IntegerField()
    max_num = models.IntegerField()
    has_decimal = models.BooleanField(default=False)
    has_negative = models.BooleanField(default=False)
    question = GenericRelation(QuestionFields, related_query_name='number')


class Link(models.Model):
    hint = models.CharField(max_length=255, null=True, blank=True)
    question = GenericRelation(QuestionFields, related_query_name='link')


class Email(models.Model):
    hint = models.CharField(max_length=255, null=True, blank=True)
    question = GenericRelation(QuestionFields, related_query_name='email')


class Text(models.Model):
    BUTTON_SHAPE = (('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'), ('5', 'Fifth'), ('6', 'Sixth'))
    button_shape = models.CharField(max_length=20, choices=BUTTON_SHAPE, null=True, blank=True)
    button_text = models.CharField(max_length=50, null=True, blank=True)
    question = GenericRelation(QuestionFields, related_query_name='text')


class File(models.Model):
    max_size = models.IntegerField(null=True, blank=True)
    question = GenericRelation(QuestionFields, related_query_name='file')


class TextWithAnswer(models.Model):
    validation = models.JSONField(null=True, blank=True)
    question = GenericRelation(QuestionFields, related_query_name='text_with_answer')


class DrawerList(models.Model):
    options = ArrayField(models.CharField(max_length=255))
    min_selection = models.PositiveIntegerField(null=True, blank=True)
    max_selection = models.PositiveIntegerField(null=True, blank=True)
    is_random_order = models.BooleanField(default=False)
    is_alphabet_order = models.BooleanField(default=False)
    question = GenericRelation(QuestionFields, related_query_name='drawer_list')


class Grading(models.Model):
    start_grade_at = models.PositiveIntegerField()
    end_grade_at = models.PositiveIntegerField()
    icon = models.ImageField(upload_to='media/', null=True, blank=True)
    question = GenericRelation(QuestionFields, related_query_name='grading')


class GroupQuestions(models.Model):
    BUTTON_SHAPE = (('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'), ('5', 'Fifth'), ('6', 'Sixth'))
    button_shape = models.CharField(max_length=20, choices=BUTTON_SHAPE, null=True, blank=True)
    button_text = models.CharField(max_length=50, null=True, blank=True)
    is_random_order = models.BooleanField(default=False)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='group_questions')
    question = GenericRelation(QuestionFields, related_query_name='group_questions_generic')


class Prioritization(models.Model):
    options = ArrayField(models.CharField(max_length=255))
    is_random_order = models.BooleanField(default=False)
    is_alphabetic_order = models.BooleanField(default=False)
    question = GenericRelation(QuestionFields, related_query_name='prioritization')


class MultiChoice(models.Model):
    options = ArrayField(models.CharField(max_length=255))
    min_selection = models.PositiveIntegerField(null=True, blank=True)
    max_selection = models.PositiveIntegerField(null=True, blank=True)
    extra_actions = models.JSONField(null=True, blank=True)
    is_random_order = models.BooleanField(default=False)
    is_alphabetic_order = models.BooleanField(default=False)
    is_vertical_display = models.BooleanField(default=False)
    is_2x_picture = models.BooleanField(default=False)
    is_select_all = models.BooleanField(default=False)
    question = GenericRelation(QuestionFields, related_query_name='multi_choice')


class WelcomePage(models.Model):
    BUTTON_SHAPE = (('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'), ('5', 'Fifth'), ('6', 'Sixth'))
    button_shape = models.CharField(max_length=20, choices=BUTTON_SHAPE, null=True, blank=True)
    button_text = models.CharField(max_length=50, null=True, blank=True)
    question = GenericRelation(QuestionFields, related_query_name='welcome_page')


class ThanksPage(models.Model):
    link = models.URLField(null=True, blank=True)
    has_social_link = models.BooleanField(default=False)
    has_eitaa = models.BooleanField(default=False)
    has_telegram = models.BooleanField(default=False)
    has_whatsapp = models.BooleanField(default=False)
    has_instagram = models.BooleanField(default=False)
    has_soroush = models.BooleanField(default=False)
    question = GenericRelation(QuestionFields, related_query_name='thanks_page')
