from django.db import models
from django.contrib.auth.models import User

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

# Define Bookmark Tag
class Tag(models.Model):
	name = models.CharField(max_length=62, unique=True)
	bookmarks = models.ManyToManyField(Bookmark)
	# Show Korean Tags in console
	def __unicode__(self):
		return self.name
