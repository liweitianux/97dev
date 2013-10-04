# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from .storage import OverwriteStorage
from .utils import avatar_by_user
from .image import crop

from sfaccount import models as am


class Profile(models.Model):

    gender_choices = (
        (0, u"男"),
        (1, u"女")
    )

    education_choices = (
        (0, u"高中"),
        (1, u"大专"),
        (2, u"本科"),
        (3, u"硕士"),
        (4, u"博士"))

    account = models.OneToOneField(am.Account, verbose_name=u"账户")
    screen_name = models.CharField(u"显示名称",
            max_length=15, blank=True)
    #user      = models.OneToOneField(User, null=True, blank=True)
    #name      = models.CharField(u"用户名", max_length=20, null=True, blank=True)
    #avatar    = models.ImageField(u"头像", upload_to="uploads/avatar/", storage=OverwriteStorage())
    education = models.IntegerField(u"学历", choices=education_choices)
    #email     = models.EmailField(u"邮箱", primary_key=True)
    gender    = models.IntegerField(u"性别", choices=gender_choices, default=0)
    user_level= models.IntegerField(u"等级", default=0)
    medicines = models.ManyToManyField("medicine.Medicine", related_name="users", verbose_name= u"药物", null=True, blank=True)
    hospital  = models.ForeignKey("location.Hospital", related_name="patients", verbose_name= u"医院", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = u"用户信息"
        
    def __unicode__(self):
        return "< Profile : %s >" % self.id

    def save(self, exist=False, *args, **kwargs):
        # 保存

        if self.id:
            exist = True
        if not exist and not self.avatar:
            # 自动生成头像
            self.avatar = avatar_by_user(self.user)
        super(Profile, self).save(*args, **kwargs)

    def thumbnail(self, size=100):
		# 头像截图
        return crop(self.avatar, self.user.id, size, flag="user")

class UserHospitalItem(models.Model):
    
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    user       = models.ForeignKey(User, verbose_name=u"用户", null=True, blank=True)
    hospital   = models.ManyToManyField("location.Hospital", related_name='userhospitalitems', verbose_name=u"就诊医院", null=True, blank=True)

    class Meta:
        verbose_name_plural=u"就诊医院记录"

    def __unicode__(self):
        return "< UserHospitalItem: %s>" % self.id


class UserReadingLog(models.Model):

    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    user       = models.ForeignKey(User, verbose_name=u"用户", null=True, blank=True)
    #sciblog   = models.ForeignKey('blog.SciBlog', related_name="readinglogs", verbose_name=u"文章")
    sciblog    = models.TextField(u"文章")              #TODO:修改成真正的sciblog外键
    readevent  = models.ManyToManyField('ReadEvent', related_name="readinglogs", verbose_name=u"阅读事件", null=True, blank=True)

    class Meta:
        verbose_name_plural=u"用户医学文章阅读记录"

    def __unicode__(self):
        return "< UserReadingLog: %s >" % self.id
    

class ReadEvent(models.Model):

    type_choices = (
        (0, "isUnd"),
        (1, "fav"),
        (2, "ask"),
        (3, "note"),)
        
    type           = models.IntegerField(u"类型", choices=type_choices, default=0)

    content_type   = models.ForeignKey(ContentType, null=True, blank=True)                   # 将ReadEvent作为GenericForeignKey
    object_id      = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name_plural=u"文章阅读事件"

    def __unicode__(self):
        return "< ReadEvent: %s >" % self.id


class Noting(models.Model):

    content        = models.TextField(u"内容")                               # TODO: 完善代码，确保能输入中文
    user           = models.ForeignKey(User, verbose_name=u"用户", null=True, blank=True)

    content_type   = models.ForeignKey(ContentType, null=True, blank=True)                         # 将ReadEvent作为GenericForeignKey
    object_id      = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey("content_type", "object_id")
    
    class Meta:
        verbose_name_plural=u"记笔记"

    def __unicode__(self):
        return "< Noting: %s >" % self.id


class UserLevelLog(models.Model):

    value      = models.FloatField(u"获得经验值")
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    user       = models.ForeignKey(User, verbose_name=u"用户", null=True, blank=True)

    class Meta:
        verbose_name_plural=u"用户等级记录"

    def __unicode__(self):
        return "< UserLevelLog: %s >" % self.id



admin.site.register([
                     Profile,
                     UserHospitalItem,
                     UserReadingLog,
                     ReadEvent,
                     Noting,
                     UserLevelLog,
                    ])
