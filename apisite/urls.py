from django.urls import path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

urlpatterns = [
    #ユーザー系
    path('users/', views.user_list),
    path('users/<int:pk>/', views.user_detail),
    path('users/<int:pk>/edit/', views.user_edit),
    path('users/<int:pk>/favorite/', views.user_favorites),
    path('users/<int:pk>/read-later/', views.user_read_later),
    path('users/<int:pk>/follow/', views.user_follow),
    path('users/<int:pk>/follower/', views.user_follower),
    path('login/', views.login),
    path('register/', views.register),

    #小説系
    path('novels/', views.novel_list),
    path('novels/<int:pk>/', views.novel_detail),
    path('novels/<int:pk>/edit/', views.novel_edit),
    path('novels/<int:pk>/delete/', views.novel_delete),
    path('novels/search/', views.novel_search),
    path('novels/favorite/', views.novel_favorite),
    path('novels/user/<int:pk>', views.novel_user),
    path('categories/', views.category_list),
    
    # comment系
    path('novels/<int:pk>/comments', views.novels_comment_list),
    path('profile/<int:pk>/comments', views.profile_comment_list),
    path('novels/<int:novel_pk>/comments/<int:user_pk>/create/', views.comment_create),
    path('novels/<int:novel_pk>/comments/<int:user_pk>/<int:comment_pk>/delete/', views.comment_delete),

    path('novels/<int:novel_pk>/comments/<int:user_pk>/<int:comment_pk>/update/', views.comment_update),
    
    #favorite系
    path('novels/<int:novel_pk>/favorites/<int:user_pk>/', views.put_favarite),


    #read later系
    path('novels/<int:novel_pk>/read-later/<int:user_pk>/', views.put_read_later),


    # その他
    path('send-email/', views.send_email),
    path('users/chat-gpt/', views.get_chatgpt_account)
]