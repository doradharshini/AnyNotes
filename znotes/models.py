from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os

class Department(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Note(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    department = models.CharField(max_length=50,default='OTHERS')
    # file = models.FileField(upload_to="files",null=True)
    def __str__(self):
        return self.title + ' by ' + str(self.author)
    
class Profile(models.Model):
    name = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=250, blank=True, null=True)
    website_link = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.CharField(max_length=100, blank=True, null=True)
    instagram_link = models.CharField(max_length=100, blank=True, null=True)
    linkedin_link = models.CharField(max_length=100, blank=True, null=True)

    profile_pic = models.ImageField(upload_to="profiles/",null=True,blank=True)
    date_modified = models.DateTimeField(User,auto_now=True)

    def __str__(self):
        return str(self.name)


def createProfile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(name = instance)
        user_profile.save()

post_save.connect(createProfile,sender = User)

class MyFile(models.Model):
    file = models.FileField(upload_to="files",null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    noteid = models.ForeignKey(Note, on_delete=models.CASCADE)
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension