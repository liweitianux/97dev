# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(u"名称", max_length=100)
    category = models.CharField(u" 种类", max_length=100, null=True, blank= True)
    pdaLink = models.CharField(u"FDA批准链接", max_length=200, null=True, blank= True)
    dosageForm = models.CharField(u"剂型", max_length=100, null=True, blank= True)
    specifications = models.ManyToManyField('Specification', related_name='medicines', verbose_name=u"药品规格", null=True, blank=True)
    company = models.ForeignKey('Company', related_name='medicines', verbose_name = u"厂家", null=True, blank=True)
    instruction = models.FileField(upload_to="upload/instructions", max_length=400, verbose_name = u"说明书", null=True, blank=True)

    class Meta:
        verbose_name_plural = u"药物"

    def __unicode__(self):
        return u"< Medicine: %s >" % self.id

class Specification(models.Model):

    value = models.FloatField(u"数值")
    unit = models.OneToOneField('indicator.Unit', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = u"药品规格"
        
    
    def __unicode__(self):
        return "< Specification: %s >" % self.id

class Company(models.Model):

    name = models.CharField(u"名称", max_length=100)
    nation = models.ForeignKey('location.Nation', related_name='companys', verbose_name = u"国家", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = u"厂家" 
    
    def __unicode__(self):
        return "< Company: %s >" % self.id
        
    

admin.site.register([
                     Medicine,
                     Specification,
                     Company,
                    ])
