from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=64, null=False)
    email = models.EmailField(max_length=256, null=False)
    affiliate = models.CharField(max_length=5)

class Preferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False)