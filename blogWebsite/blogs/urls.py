from django.urls import include,path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
#Paths
urlpatterns = [
    path('profile/login',obtain_auth_token),
    path('profile/logout',views.logout_profile),
    path('profile',views.profile_view),
    path('profile',views.profile_view),
    path('profile/<str:username>',views.profile_view),

    path('profile-list',views.profile_list_view),

    path('blog-list',views.bloglist_view),
    path('blog-list/<str:username>', views.view_blogs_from_user),
    path('blog',views.blog_view),
    path('blog/<int:blog_id>',views.blog_view),
    
    


    path('follower',views.follower_view),
    #path('<str:username>/get_followers',views.get_followers)
   

]