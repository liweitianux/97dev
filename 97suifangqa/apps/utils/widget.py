# -*- coding: utf8 -*-
from django import forms
class MarkitUpWidget(forms.Textarea):
    u'''
    一个将textarea改造成markitup的widget
    '''
    class Media:
        js = (
            'jquery-1.9.1.min.js',
            'markitup/jquery.markitup.js',
            'markitup/sets/markdown/set.js',
            'markitup/markItUp_init.js',
        )

        css = {
            'screen': (
                'markitup/skins/simple/style.css',
                'markitup/sets/markdown/style.css',
            )
        }


class TinyMceWidget(forms.Textarea):
    u'''
    一个将textarea改造成tinymce编辑器的widget
    '''

    class Media:
        js = (
            'jquery-1.9.1.min.js',
            'tinymce/js/tinymce/tinymce.min.js',
            'tinymce/js/tinymce/tinymce_init.js',
        )
        
        css = {
            'screen': (
                'tinymce/css/custom_tinymce.css',
            )
        }

