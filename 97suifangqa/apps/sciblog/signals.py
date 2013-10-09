# -*- coding: utf-8 -*-

from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from sciblog.models import (
        SciBlog, BlogAnnotation, ResultContent, Reference, BaseLine,
        ClinicCondition, KnowledgePiece, Guideline, EndPoint
)

import re

def mark_keywords_in_textfield(model, fields, related_name='NONE'):
    u'''
    fields:需要处理的field名称
    handler:消息处理函数，对instance中的fields进行关键词过滤
    related_name:model实例在BlogAnnotation中的反向关系名称,如文章注释通过blogs属性关联到Sciblog
    '''

    @receiver(pre_save, sender = model, weak=False)
    def handler(sender, **kwargs):
        instance = kwargs['instance']
        for annotation in BlogAnnotation.objects.propernouns():
            keyword = annotation.firstkeyword()
            for field in set(fields):
                content = getattr(instance, field)
                if keyword not in content:
                    continue
                try:
                    relate = getattr(annotation, related_name)
                    relate.add(instance)
                    annotation.save()
                except:
                    pass

mark_keywords_in_textfield(SciBlog, ['abstract_result', 'method', 'aim', 
                                     'abstractAE', 'treatment_content', 
                                     'endpoint_content', 'detectionAssay'], 'blogs')
mark_keywords_in_textfield(ResultContent, ['abstract', 'content', 'card_content'])
mark_keywords_in_textfield(Reference, ['description'])
mark_keywords_in_textfield(KnowledgePiece, ['content'])
mark_keywords_in_textfield(Guideline, ['content'])
mark_keywords_in_textfield(EndPoint, ['content'])
mark_keywords_in_textfield(ClinicCondition, ['content'])
mark_keywords_in_textfield(BaseLine, ['content'])

def mark_keywords_in_m2mfields(sender, **kwargs):
    if kwargs['action'] != 'pre_add':
        return 
    blog = kwargs['instance']
    model = kwargs['model']
    objs = model.objects.filter(pk__in = kwargs.get('pk_set') or [])
    for annotation in BlogAnnotation.objects.propernouns():
        keyword = annotation.firstkeyword()
        for obj in objs:
            if keyword not in obj.content:
                continue
            annotation.blogs.add(blog)
            annotation.save()
            return 

for m2m in ['konwledge_piece', 'baseline', 'endpoints', 'clinic_conditions']:
    m2m_changed.connect(mark_keywords_in_m2mfields, sender=getattr(SciBlog, m2m).through)
