#-*- coding: utf-8 -*-
"""
	文件存储
"""
import os
import time 
import random

from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        fn = time.strftime("%Y%m%d%H%M%S")
        fn = fn + "_%d" % random.randint(0,1000)
        name = os.path.join(d, fn + ext)
        return super(OverwriteStorage, self)._save(name, content)