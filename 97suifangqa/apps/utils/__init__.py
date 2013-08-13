# -*- coding: utf8 -*-

def get_abstract(long_str, max_length=20):
    u'''
    获得一个长字符串的摘要
    算法：取前max_length个字符，或者取第一个标点符号之前的字符串，哪一种更短，取哪一种
    '''

    max_length = min(len(long_str), max_length)
    return long_str[0:max_length]

