from django.db import models

# Create your models here.
class Content(models.Model):
	link = models.CharField(max_length = 100, null = True, blank = True)


class UserContent(models.Model):
	user = models.ForeignKey('users.UserProfile')
	content = models.ForeignKey(Content)
