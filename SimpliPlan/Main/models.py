from django.db import models
from django.db.models import Q

class UserManager(models.Manager):
    def validate(self,username,password):
        return self.get_queryset().filter(username=username, password=password)

    def exist(self,username,email):
        return self.get_queryset().filter(Q(username=username) | Q(email=email))

    def verify(self,username):
        return self.get_queryset().filter(username=username)
    
class User(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user = UserManager() 