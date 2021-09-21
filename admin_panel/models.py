from django.db import models
import datetime


# ADMIN USERS
class AdminUser(models.Model):
	username = models.CharField(max_length=50,null=True,blank=True)
	password = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.username
