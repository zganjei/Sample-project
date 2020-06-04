import datetime

from django.core.exceptions import ValidationError
from django.db import models


# from conf.models import GlobalConfig


class Titled(models.Model):
    title = models.CharField(verbose_name="عنوان", max_length=500)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class CreateLog(models.Model):
    creator = models.ForeignKey('account.User', verbose_name="سازنده", null=True, blank=True,
                                related_name='%(class)s_creators', on_delete=models.SET_NULL)
    created_on = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        abstract = True

    @property
    def created_time(self):
        return self.created_on.strftime("%H:%M:%S")

    @property
    def created_timestamp(self):
        return int(self.created_on.timestamp())


class ModifyLog(models.Model):
    modifier = models.ForeignKey('account.User', verbose_name="ویرایش کننده", null=True, blank=True,
                                 related_name='%(class)s_modifiers', on_delete=models.SET_NULL)
    modify_on = models.DateTimeField(verbose_name="تاریخ ویرایش", auto_now=True)

    class Meta:
        abstract = True

    @property
    def modify_time(self):
        now = datetime.datetime.utcnow()
        today_zero = datetime.datetime.combine(now, datetime.time(0, 0))
        sec = (today_zero - self.modify_on.replace(tzinfo=None)).total_seconds()
        if sec < 0:
            return (self.modify_on.replace(tzinfo=None) + datetime.timedelta(hours=3, minutes=30)).strftime("%H:%M")
        elif sec < DAY_SEC * 7:
            days = int(sec / DAY_SEC)
            if days < 2:
                return "دیروز"
            elif days == 2:
                return "پریروز"
            return "%s روز قبل" % days
        else:
            return "%s هفته قبل" % int(sec / WEEK_SEC)

    @property
    def modified_time(self):
        return int(self.modify_on.timestamp() * 1000)


DAY_SEC = 60 * 60 * 24
WEEK_SEC = 60 * 60 * 24 * 7
YEAR_SEC = 60 * 60 * 24 * 7 * 54


class LoggableModel(CreateLog, ModifyLog):
    class Meta:
        abstract = True


class Certifiable(models.Model):
    confirm = models.BooleanField(verbose_name="تاییدشده", default=False)

    class Meta:
        abstract = True


class VisitorTrack(models.Model):
    visitor_count = models.IntegerField("تعداد بازدید", default=0)

    class Meta:
        abstract = True

    def add_visit(self):
        self.visitor_count += 1
        self.save()


# def image_size_validate(image):
#     file_size = image.file.size
#     max_image_size = GlobalConfig.get_config().max_image_upload
#     if file_size > max_image_size * 1024 * 1024:
#         raise ValidationError("حداکثر حجم تصویر باید %s مگابایت باشد" % max_image_size)


def get_client_ip(request):
    # return get_ip(request)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
