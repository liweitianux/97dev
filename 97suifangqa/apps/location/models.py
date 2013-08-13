#-*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin


class Location(models.Model):

	latitude = models.FloatField(u"经度")
	longitude = models.FloatField(u"纬度")
	city = models.CharField(u"城市", max_length=20, null=True, blank=True)
	nation = models.CharField(u"国家", max_length=20, null=True, blank=True)

	class Meta:
		verbose_name_plural = u"地理位置"

	def __unicode__(self):
		return u"< Location : %s >" % self.id


class Hospital(models.Model):

    name = models.CharField(u"名称", max_length=100)
    city = models.ForeignKey("City", related_name="hospitals", verbose_name = u"城市", null=True, blank=True)
    unit = models.ForeignKey("indicator.Unit", related_name="hospitals", verbose_name = u"单位", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"医院"

    def __unicode__(self):
        return "< Hospital: %s >" % self.name


class City(models.Model):

    name = models.CharField(u"名称", max_length=100)
    nation = models.ForeignKey("Nation", related_name="cities", verbose_name = "国家", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"城市"

    def __unicode__(self):
        return "< City: %s >" % self.name


class Nation(models.Model):

    name = models.CharField(u"名称", max_length=100)
    img = models.ImageField(u"国旗图标", upload_to="uploads/flags/", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"国家"

    def __unicode__(self):
        return "< Nation: %s >" % self.name


admin.site.register([
                     Location,
                     Hospital,
                     City,
                     Nation,
                    ])
