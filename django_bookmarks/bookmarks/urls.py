from django.conf.urls import url
urlpatterns = [
		url(r'^recents/$', 'bookmarks.view.RecentBookmarks'),
]
