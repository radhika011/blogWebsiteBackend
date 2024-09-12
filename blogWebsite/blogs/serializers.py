from xml.dom import ValidationErr
from rest_framework import serializers

from .models import Blogpost, Follower,Profile
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
class BlogpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogpost
        fields = "__all__"







class ProfileSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Profile
        fields = ('first_name','last_name','username','bio','password')
        #lookup_field = "username"



class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = "__all__"
        
