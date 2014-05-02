# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django_bookmarks.bookmarks.models import Bookmark
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# p.175 error occurred : Page not Found Error : please refer urls.py
class UserBookmarks(Feed):
	def get_object(self, bits):
		if bits.len() != 1:
			raise ObjectDoesNotExist
		return User.objects.get(username=bits[0])

	def title(self, user):
		return u'장고 북마크 | %s가 등록한 북마크' % user.username

	def link(self, user):
		return '/feeds/user/%s/' % user.username

	def description(self, user):
		return u'장고 북마크 서비스를 통해서 %s가 등록한 북마크' % user.username

	def items(self, user):
		return user.bookmark_set.order_by('-id')[:10]

class RecentBookmarks(Feed):
	title = u'장고 북마크 | 최신 북마크'
	link = '/feeds/recent/'
	description = u'장고 북마크 서비스를 통해서 등록된 북마크'
	
	def items(self):
		return Bookmark.objects.order_by('-id')[:10]
