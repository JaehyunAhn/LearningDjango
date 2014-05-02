from django.conf.urls import url
from django_bookmarks.bookmarks.feeds import *

urlpatterns = [
		url(r'^recents/$', RecentBookmarks()),
		url(r'^user/$', UserBookmarks()),
]

# ERROR was occurred!
