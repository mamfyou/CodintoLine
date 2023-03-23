from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

BUTTON_SHAPE = (('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'), ('5', 'Fifth'), ('6', 'Sixth'))


class Range(models.Model):
    start_range_at = models.PositiveIntegerField(verbose_name='شروع بازه')
    end_range_at = models.PositiveIntegerField(verbose_name='پایان بازه')
    right_tag = models.CharField(max_length=50, blank=True, null=True, verbose_name='برچسب راست')
    mid_tag = models.CharField(max_length=50, blank=True, null=True, verbose_name='برچسب میانی')
    left_tag = models.CharField(max_length=50, blank=True, null=True, verbose_name='برچسب چپ')
    has_zero = models.BooleanField(default=False)


class Number(models.Model):
    min_num = models.IntegerField(verbose_name='حداقل عدد')
    max_num = models.IntegerField(verbose_name='حداکثر عدد')
    has_decimal = models.BooleanField(default=False, verbose_name='اعشار دارد')
    has_negative = models.BooleanField(default=False, verbose_name='منفی دارد')


class Link(models.Model):
    hint = models.CharField(max_length=255, null=True, blank=True, verbose_name='راهنمایی')


class Email(models.Model):
    hint = models.CharField(max_length=255, null=True, blank=True, verbose_name='راهنمایی')


class Text(models.Model):
    button_shape = models.CharField(max_length=20, choices=BUTTON_SHAPE, null=True, blank=True, verbose_name='شکل دکمه')
    button_text = models.CharField(max_length=50, null=True, blank=True, verbose_name='متن دکمه')


class File(models.Model):
    max_size = models.IntegerField(null=True, blank=True, verbose_name='حداکثر حجم فایل')


class TextWithAnswer(models.Model):
    validation = models.JSONField(null=True, blank=True, verbose_name='اعتبارسنجی')


class DrawerList(models.Model):
    min_selection = models.PositiveIntegerField(null=True, blank=True, verbose_name='حداقل انتخاب')
    max_selection = models.PositiveIntegerField(null=True, blank=True, verbose_name='حداکثر انتخاب')
    is_random_order = models.BooleanField(default=False, verbose_name='ترتیب تصادفی')
    is_alphabetic_order = models.BooleanField(default=False, verbose_name='ترتیب بر اساس حروف الفبا')


class Grading(models.Model):
    DEFAULT_ICON = (
        ('like', 'Like_Button'), ('star', 'Star_Button'), ('heart', 'Heart_Button'), ('tick', 'Tick_Button'))
    default_icon = models.CharField(max_length=20, null=True, blank=True, choices=DEFAULT_ICON, verbose_name='آیکون پیش فرض')
    end_grade_at = models.PositiveIntegerField(verbose_name='پایان بازه')
    icon = models.ImageField(upload_to='media/', null=True, blank=True, verbose_name='آیکون دلخواه')


class GroupQuestions(models.Model):
    button_shape = models.CharField(max_length=20, choices=BUTTON_SHAPE, null=True, blank=True, verbose_name='شکل دکمه')
    button_text = models.CharField(max_length=50, null=True, blank=True, verbose_name='متن دکمه')
    is_random_order = models.BooleanField(default=False, verbose_name='ترتیب تصادفی')


class Prioritization(models.Model):
    is_random_order = models.BooleanField(default=False, verbose_name='ترتیب تصادفی')
    is_alphabetic_order = models.BooleanField(default=False, verbose_name='ترتیب بر اساس حروف الفبا')


class MultiChoice(models.Model):
    min_selection = models.PositiveIntegerField(null=True, blank=True, verbose_name='حداقل انتخاب')
    max_selection = models.PositiveIntegerField(null=True, blank=True, verbose_name='حداکثر انتخاب')
    extra_actions = models.JSONField(null=True, blank=True, verbose_name='گزینه اضافی')
    is_random_order = models.BooleanField(default=False, verbose_name='ترتیب تصادفی')
    is_alphabetic_order = models.BooleanField(default=False, verbose_name='ترتیب بر اساس حروف الفبا')
    is_vertical_display = models.BooleanField(default=False, verbose_name='نمایش عمودی')
    is_2x_picture = models.BooleanField(default=False, verbose_name='نمایش دو برابر عکس')
    is_select_all = models.BooleanField(default=False, verbose_name='انتخاب همه')


class WelcomePage(models.Model):
    button_shape = models.CharField(max_length=20, choices=BUTTON_SHAPE, null=True, blank=True, verbose_name='شکل دکمه')
    button_text = models.CharField(max_length=50, null=True, blank=True, verbose_name='متن دکمه')


class ThanksPage(models.Model):
    short_url_uuid = models.CharField(unique=True, max_length=255, editable=False, verbose_name='آیدی پیچیده پرسشنامه')
    has_social_link = models.BooleanField(default=False, verbose_name='لینک شبکه های اجتماعی')
    has_eitaa = models.BooleanField(default=False, verbose_name='ایتا')
    has_telegram = models.BooleanField(default=False, verbose_name='تلگرام')
    has_whatsapp = models.BooleanField(default=False, verbose_name='واتساپ')
    has_instagram = models.BooleanField(default=False, verbose_name='اینستاگرام')
    has_soroush = models.BooleanField(default=False, verbose_name='سروش')


class Option(models.Model):
    name = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='media/', null=True, blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='options')
