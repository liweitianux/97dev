#-*- coding: utf-8 -*-

import random

from django.conf import settings


def avatar_by_user(user):
	"""
		生成头像
	"""
	from django.core.files.images import ImageFile

	_avatar_path = "%s/avatars/%s.png" % (settings.MEDIA_ROOT, random.randint(1,22))

	_avatar = ImageFile(open(_avatar_path))
	user.profile.avatar = _avatar
	user.profile.save()
	return user.profile