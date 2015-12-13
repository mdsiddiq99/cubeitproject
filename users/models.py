from django.db import models

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField('auth.User', null = True)
	name = models.CharField(max_length = 100, null = True, blank = True)
	city = models.CharField(max_length = 100, null = True, blank = True)
