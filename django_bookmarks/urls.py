import os.path
from django.conf.urls import patterns, include, url
from bookmarks.views import *
from django.contrib import admin
from django.views.generic import TemplateView
from bookmarks.feeds import *

admin.autodiscover()

site_media = os.path.join(
		os.path.dirname(__file__), 'site_media'
)

urlpatterns = patterns('',
	# Feeds
	(r'^feeds/', RecentBookmarks()),
	# Ajax
	(r'^ajax/tag/autocomplete/$',ajax_tag_autocomplete),
	# Browsing
	(r'^popular/$', popular_page),
	# Main page
	(r'^$', main_page),
	# Admin page
	(r'^admin/', include(admin.site.urls)),
	# old version 1.2 (r'^admin/(.*)', admin.site.root),
	# Comments
	(r'^comments/', include('django.contrib.comments.urls')),
	(r'^bookmark/(\d+)/$', bookmark_page),
	# User Page
	(r'^user/(\w+)/$', user_page),
	(r'^login/$','django.contrib.auth.views.login'),
	(r'^logout/$', logout_page),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
		{ 'document_root': site_media }),
	(r'^register/$', register_page),
	# old version 1.2 below
	# (r'^register/success/$',direct_to_template, 'template':'regestration/register_success.html'}),
	(r'^register/success/$',TemplateView.as_view(template_name="registration/register_success.html")),
	# Account Management
	(r'^save/$', bookmark_save_page),
	(r'^vote/$', bookmark_vote_page),
	(r'^tag/([^\s]+)/$',tag_page),
	(r'^tag/$',tag_cloud_page),
	(r'^search/$', search_page),
)
