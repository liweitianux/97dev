# -*- coding: utf-8 -*-

"""
models for apps/recommend
"""


from django.db import models
from django.contrib import admin


class TreatRespnse(models.Model):                           # {{{
    """
    治疗反应/结果的描述，以及结果的价值/权重
    """
    name = models.CharField(u"名称", max_length=100)
    description = models.TextField(u"详细描述", blank=True)
    weight = models.FloatField(u"权重", help_text=u"范围：0-10")
    # datetime
    created_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(u"更新时间",
            auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name_plural = u"治疗反应"

    def __unicode__(self):
        return u"< TreatRespnse: %s >" % self.name

    def save(self, **kwargs):
        if self.is_valid():
            super(TreatRespnse, self).save(**kwargs)
        else:
            return self

    def is_valid(self, **kwargs):
        # check weight range
        if (self.weight < 0.0) or (self.weight > 10.0):
            print u"Error: weight < 0.0 / weight > 10.0"
            return False
        #
        return True
# }}}


# admin
admin.site.register([
    TreatRespnse,
])

