from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
BUTTON_SHAPE = (('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'), ('5', 'Fifth'), ('6', 'Sixth'))


class Range(models.Model):
    start_range_at = models.PositiveIntegerField()
    end_range_at = models.PositiveIntegerField()
    first_tag = models.CharField(max_length=50, blank=True, null=True)
    mid_tag = models.CharField(max_length=50, blank=True, null=True)
    end_tag = models.CharField(max_length=50, blank=True, null=True)
    has_zero = models.BooleanField(default=False)


class Number(models.Model):
    min_num = models.IntegerField()
    max_num = models.IntegerField()
    has_decimal = models.BooleanField(default=False)
    has_negative = models.BooleanField(default=False)


class Link(models.Model):
    hint = models.CharField(max_length=255, null=True, blank=True)


class Email(models.Model):
    hint = models.CharField(max_length=255, null=True, blank=True)


class Text(models.Model):
    button_shape = models.CharField(max_length=20, choices=BUTTON_SHAPE, null=True, blank=True)
    button_text = models.CharField(max_length=50, null=True, blank=True)


class File(models.Model):
    max_size = models.IntegerField(null=True, blank=True)


class TextWithAnswer(models.Model):
    validation = models.JSONField(null=True, blank=True)


class DrawerList(models.Model):
    options = ArrayField(models.CharField(max_length=255))
    options_pic = ArrayField(models.ImageField(upload_to='media/', null=True, blank=True))
    min_selection = models.PositiveIntegerField(null=True, blank=True)
    max_selection = models.PositiveIntegerField(null=True, blank=True)
    is_random_order = models.BooleanField(default=False)
    is_alphabet_order = models.BooleanField(default=False)


class Grading(models.Model):
    start_grade_at = models.PositiveIntegerField()
    end_grade_at = models.PositiveIntegerField()
    icon = models.ImageField(upload_to='media/', null=True, blank=True)


class GroupQuestions(models.Model):
    button_shape = models.CharField(max_length=20, choices=BUTTON_SHAPE, null=True, blank=True)
    button_text = models.CharField(max_length=50, null=True, blank=True)
    is_random_order = models.BooleanField(default=False)


class Prioritization(models.Model):
    options = ArrayField(models.CharField(max_length=255))
    options_pic = ArrayField(models.ImageField(upload_to='media/', null=True, blank=True))
    is_random_order = models.BooleanField(default=False)
    is_alphabetic_order = models.BooleanField(default=False)


class MultiChoice(models.Model):
    options = ArrayField(models.CharField(max_length=255))
    options_pic = ArrayField(models.ImageField(upload_to='media/', null=True, blank=True))
    min_selection = models.PositiveIntegerField(null=True, blank=True)
    max_selection = models.PositiveIntegerField(null=True, blank=True)
    extra_actions = models.JSONField(null=True, blank=True)
    is_random_order = models.BooleanField(default=False)
    is_alphabetic_order = models.BooleanField(default=False)
    is_vertical_display = models.BooleanField(default=False)
    is_2x_picture = models.BooleanField(default=False)
    is_select_all = models.BooleanField(default=False)


class WelcomePage(models.Model):
    button_shape = models.CharField(max_length=20, choices=BUTTON_SHAPE, null=True, blank=True)
    button_text = models.CharField(max_length=50, null=True, blank=True)


class ThanksPage(models.Model):
    link = models.URLField(null=True, blank=True)
    has_social_link = models.BooleanField(default=False)
    has_eitaa = models.BooleanField(default=False)
    has_telegram = models.BooleanField(default=False)
    has_whatsapp = models.BooleanField(default=False)
    has_instagram = models.BooleanField(default=False)
    has_soroush = models.BooleanField(default=False)




