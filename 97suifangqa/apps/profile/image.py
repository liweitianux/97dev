# -*- coding: utf-8 -*-
"""
	图片处理函数
"""
import os
import time

from hashlib import md5
from django.conf import settings
from os import mkdir, path as _path

try:
	from PIL import Image, ImageOps, ImageDraw
except:
	import Image, ImageOps, ImageDraw


def rm_avatar_thumb(object_id, avatar_link):
	name, ext = _path.splitext(avatar_link)
	try:
		fn = generat_location(object_id, ext, 200)
		os.remove(fn)
	except:
		pass
	

def _mkdir(dirname):
	"""
		遍历创建文件夹
	"""
	index = []
	initial = 0
	for i in range(dirname.count('/')):
		initial = dirname.find('/', initial, len(dirname))
		index.insert(len(index), initial)
		initial += 1
	for j in index[1:]:
		_dir = dirname[:j]
		if _dir and not _path.exists(_dir):
			mkdir(_dir)


def generat_dir_and_fn(uid, flag):
	root = settings.MEDIA_ROOT
	fn = md5('%s' % uid).hexdigest()
	d1 = fn[-2:]
	d2 = fn[-4:-2]
	dirname = "%s%s/%s/%s/" % (root, flag, d1, d2)
	return dirname, fn


def generat_location(uid, ext, size, flag):
	"""
		获取文件路径
	"""
	fmt = "%s%s_%s%s"
	dirname, fn = generat_dir_and_fn(uid, flag)
	_mkdir(dirname)
	if not ext or \
		ext == '.':
		ext = '.jpg'
	return fmt % (dirname, fn, size, ext)


def crop(image, object_id, size=100, mask_img=None, flag="cache", **kwargs):
	"""
		截取图片
	"""
	_size = (size, size)
	path = image.path
	root, filename = _path.split(path)
	name, ext = _path.splitext(filename)

	original = Image.open(open(path, 'rb'))

	# 保存为圆形缩略图
	"""
	mask = Image.new('L', _size, 0)
	draw = ImageDraw.Draw(mask) 
	draw.ellipse((0, 0) + _size, fill=255)
	thumb = ImageOps.fit(original, mask.size, centering=(0.5, 0.5))
	thumb.putalpha(mask)
	"""
	try:
		if mask_img:
			mask = Image.open(mask_img).convert('L')
			thumb = ImageOps.fit(original, _size, centering=(0.5, 0.5))
			thumb.putalpha(mask)
		else: thumb = ImageOps.fit(original, _size, Image.ANTIALIAS)
		
		thumb_path = generat_location(object_id, ext, size, flag)
		if not _path.exists(thumb_path):
			thumb.save(thumb_path)
	except:
		thumb_path = path
		
	return thumb_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)