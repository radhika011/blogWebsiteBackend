from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from sqlalchemy import ForeignKey
# Create your models here.




class Profile(AbstractUser):
    #username = models.CharField('username',max_length=12,primary_key=True)
    #user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    bio = models.CharField('bio',max_length=50)
    following = models.ManyToManyField("self",symmetrical=False,through='Follower')
    USERNAME_FIELD = 'username'


class Follower(models.Model):
    from_profile = models.ForeignKey(Profile,to_field="username",db_column="from_profile",on_delete=models.CASCADE,related_name="from_profile")
    to_profile = models.ForeignKey(Profile,to_field="username",db_column="to_profile",on_delete=models.CASCADE)

class Blogpost(models.Model):
    class Meta:
        unique_together = ('profile_username','datetime_published')
    profile_username = models.ForeignKey(Profile,on_delete=models.CASCADE,to_field="username",db_column="profile_username")
    title = models.CharField('title',max_length=25)
    content = models.CharField('content',max_length=500)
    datetime_published = models.DateTimeField('datetime_published',auto_now_add=True)
    likes = models.IntegerField(default=0)




    




@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)