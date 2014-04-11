import os.path
from django.conf.urls import patterns, include, url
from bookmarks.views import *
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

site_media = os.path.join(
		os.path.dirname(__file__), 'site_media'
)

urlpatterns = patterns('',
	(r'^$', main_page),
	(r'^user/(\w+)/$', user_page),
	(r'^login/$','django.contrib.auth.views.login'),
	(r'^logout/$', logout_page),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
		{ 'document_root': site_media }),
	(r'^register/$', register_page),
	# old version 1.2 below
	# (r'^register/success/$',direct_to_template, 'template':'regestration/register_success.html'}),
	(r'^register/success/$',TemplateView.as_view(template_name="registration/register_success.html")),
	(r'^save/$', bookmark_save_page),
	(r'^tag/([^\s]+)/$',tag_page),
	(r'^tag/$',tag_cloud_page),
	(r'^search/$', search_page),
)
