xpinyin

translate chinese hanzi to pinyin by python, inspired by flyerhzm’s chinese_pinyin gem
https://github.com/lxneng/xpinyin

* Install

pip install xpinyin

* Usage

In [1]: from xpinyin import Pinyin

In [2]: p = Pinyin()

In [3]: p.get_pinyin(u"上海")
Out[3]: 'shanghai'

In [4]: p.get_pinyin(u"上海", '-')
Out[4]: 'shang-hai'

In [5]: p.get_pinyin(u"上海", ' ')
Out[5]: 'shang hai'

In [6]: p.get_initials(u"上")
Out[6]: 'S'

请输入utf8编码汉字

------------------------------------------------------------------------

translate chinese hanzi to pinyin by python, inspired by flyerhzm’s
`chinese\_pinyin`_ gem

usage
-----
::
    In [1]: from xpinyin import Pinyin
    In [2]: p = Pinyin()
    In [3]: p.get_pinyin(u"上海")
    Out[3]: 'shang-hai'
    In [4]: p.get_initials(u"上")
    Out[4]: 'S'
请输入utf8编码汉字
.. _chinese\_pinyin: https://github.com/flyerhzm/chinese_pinyin

--------------------------------------------------------------------

ChangeLogs:

2013/07/28, LIweitiaNux <liweitianux@gmail.com>
  * add method 'get_initial()', support string with more than 1 char
  * add method 'get_py()', to get the initial letters of pinyin

