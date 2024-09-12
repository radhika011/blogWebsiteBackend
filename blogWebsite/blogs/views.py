from pickle import NONE
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from requests import delete

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication


from rest_framework.parsers import JSONParser
from sqlalchemy import JSON

from .serializers import BlogpostSerializer, FollowerSerializer, ProfileSerializer
from .models import Blogpost, Follower, Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
# Create your views here.

def greet(request):
    return HttpResponse("Hello World!")

################################   PROFILE VIEWS      #########################



@api_view(['GET','POST'])
@permission_classes([])
def profile_view(request,username=None):
    """
    Create, retrieve user profile
    """

    if request.method == 'GET':
        if(request.user==AnonymousUser):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if username == None:
            profile_info = Profile.objects.filter(username=request.user)
        else:
            profile_info = Profile.objects.filter(username=username)
        serializer = ProfileSerializer(profile_info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)




    if request.method == 'POST':
        profile_info = JSONParser().parse(request)
        print(profile_info)
        serializer = ProfileSerializer(data = profile_info)
        print(serializer.is_valid())
        if serializer.is_valid():
            #serializer.validated_data.user.password = make_password(serializer.validated_data.user.password)
            serializer.validated_data["password"] = make_password(serializer.validated_data["password"])
            #print(type(serializer.validated_data))
            
            serializer.save()
            user_id = Profile.objects.get(username=serializer.data['username']).id
            
            token = Token.objects.get(user=user_id).key
            serializer.data["token"] = token
            
            return Response({"token":token},status = status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile_by_user(request,username):
    
    
    #Retrieve user profile by username
    
   
    profile_info = Profile.objects.filter(username=username)
    serializer = ProfileSerializer(profile_info,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_list_view(request):
    profile_info = Profile.objects.filter() #get returns only one record
    serializer = ProfileSerializer(profile_info,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)





@api_view(['POST'])
def logout_profile(request):
    request.user.auth_token.delete()
    return Response({"user":"logged out"},status = status.HTTP_200_OK)



    
    

################################   BLOG VIEWS      #########################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_blogs_from_user(request,username):
    user_blogs = Blogpost.objects.filter(profile_username=username).order_by('-datetime_published')
    serializer = BlogpostSerializer(user_blogs,many=True)
    return Response(serializer.data,status = status.HTTP_200_OK)


@api_view(['POST','DELETE','GET'])
@permission_classes([IsAuthenticated])
def blog_view(request,blog_id = None):
    """
    Create, delete and retrieve blog posts
    
    """
    if request.method == 'POST':
        json_req = JSONParser().parse(request)
        json_req["profile_username"] = request.user
        serializer = BlogpostSerializer(data = json_req)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            #print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if blog_id == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        blogpost_info = Blogpost.objects.get(id = blog_id,profile_username=request.user)   #COVER CASE WHERE BLOG POST DOES NOT EXIST
        blogpost_info.delete()
        return Response(status=status.HTTP_200_OK)
    
    if request.method == 'GET':
        if blog_id == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        blogpost_info = Blogpost.objects.filter(id = blog_id)
        serializer = BlogpostSerializer(blogpost_info,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bloglist_view(request):
    """
    Retrieve the blogpost feed for a user.
    
    """
    if request.method == 'GET':
        following_info = Follower.objects.filter(from_profile = request.user)  #get the 'following' list of the user
        all_following = []
        for follower in following_info:
            all_following.append(follower.to_profile.username)
        print(all_following)
        user_blogs = Blogpost.objects.filter(profile_username__in=all_following).order_by('-datetime_published')
        serializer = BlogpostSerializer(user_blogs,many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)





################################   FOLLOWER VIEWS      #########################



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follower_view(request):
    follower_info = JSONParser().parse(request)
    follower_info["from_profile"] = request.user
    serializer = FollowerSerializer(data = follower_info)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
