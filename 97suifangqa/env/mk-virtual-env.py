#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
    用法：
    1. 安装：在mk-virtua-env.py文件所在目录下执行python mk-virtualenv-env.py以安装环境
    2. 运行：在terminal里面执行source <PROJ-DIR>/env/env/bin/activate, 然后启动web服务相关的进程
'''
import virtualenv, textwrap
import os,subprocess, tempfile
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess
def after_install(options, home_dir):
    subprocess.call([join(home_dir, 'bin', 'pip'),
                     'install',
                     '-r',
                     'requirements.pip'])
"""))
f = tempfile.NamedTemporaryFile()
f.write(output)
f.flush()

subprocess.call(['python', f.name, 'env'])
