from django.db import models

# Create your models here.
class Cube(models.Model):
	name  = models.CharField(max_length = 100, null = True, blank = True)


class CubeContent(models.Model):
	cube = models.ForeignKey(Cube)
	content = models.ForeignKey('contents.Content')

class UserCube(models.Model):
	user = models.ForeignKey('users.UserProfile')
	cube = models.ForeignKey(Cube)
