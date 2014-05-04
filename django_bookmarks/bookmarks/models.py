from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Define 'Link' class that inherits 'models'
class Link(models.Model): 
	url = models.URLField(unique=True)
	# Show Korean Tags in console
	def __unicode__(self):
		return self.url

# Define Bookmark Class
class Bookmark(models.Model):
	title = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	link = models.ForeignKey(Link)
	# Show Korean Tags in console
	def __unicode__(self):
		return '%s, %s' % (self.user.username, self.link.url)
	# Objects to Feed
	def get_absolute_url(self):
		return self.link.url

# Define Bookmark Tag
class Tag(models.Model):
	name = models.CharField(max_length=62, unique=True)
	bookmarks = models.ManyToManyField(Bookmark)
	# Show Korean Tags in console
	def __unicode__(self):
		return self.name

# Shared Bookmark model p.130
class SharedBookmark(models.Model):
	bookmark = models.ForeignKey(Bookmark, unique=True)
	date = models.DateTimeField(auto_now_add=True)
	votes = models.IntegerField(default=1)
	users_voted = models.ManyToManyField(User)

	def __unicode__(self):
		return '%s, %s' % (self.bookmark, self.votes)

# Social Network Model
class Friendship(models.Model):
	from_friend = models.ForeignKey(
			User, related_name = 'friend_set'
	)
	to_friend = models.ForeignKey(
			User, related_name = 'to_friend_set'
	)

	def __unicode__(self):
		return '%s, %s' % (
				self.from_friend.username,
				self.to_friend.username
		)
	class Meta:
		unique_together = (('to_friend', 'from_friend'), )
