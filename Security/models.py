from django.db import models

# Create your models here.
class s2fa_data(models.Model):
	username = models.TextField()
	s2fa_id = models.TextField()
	