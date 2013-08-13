# -*- coding: utf-8 -*-
import json
from django.db import models
from django.contrib.auth.models import AnonymousUser

class AnnotationManager(models.Manager):
    use_for_related_fields = True

    def paracomments(self):
        u'''
        获取段落注释
        '''
        return self.filter(type = 0)

    def propernouns(self):
        u'''
        获取专有名词
        '''
        return self.filter(type = 1)
    
    def all_json(self, user = AnonymousUser()):
        u'''
        通过json格式获取专有名词和段落注释
        '''
        result = {p.id:{'id':p.id,
                        'name':p.firstkeyword() if p.type == 1 else p.brief_content,
                        'type':p.type,
                        'content':p.detail,
                        'collected_times':p.collected_by.count(),
                        'is_collected': p.is_collected_by(user)} 
                  for p in self.all()}
        return  json.dumps(result)
    

class KnowledgePieceManager(models.Manager):
    use_for_related_fields = True

    def knowledges(self):
        u'''
        获取科普知识类型的条目
        '''
        return self.filter(type = 0)

    def comments(self):
        u'''
        获取科学评论类型的条目
        '''
        return self.filter(type = 1)


class EndPointManager(models.Manager):
    use_for_related_fields = True
    
    def primary(self):
        u'''
        获取主要治疗终点
        '''
        return self.filter(type = 1)

    def secondary(self):
        u'''
        获取次要治疗终点
        '''
        return self.filter(type = 2)


class ClinicConditionManager(models.Manager):
    use_for_related_fields = True

    def inclusive(self):
        u'''
        获取允许类型的临床条件
        '''
        return self.filter(type = 0)

    def exclusive(self):
        u'''
        获取排除类型的临床条件
        '''
        return self.filter(type = 1)
