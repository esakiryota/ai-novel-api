from django.contrib.auth.models import Group
from .models import Category, Novel, Right, Comment, RightToUser, User
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at']

class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'pk', 'self_introduction', 'created_at']

class UserChildSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'pk', 'self_introduction', 'created_at']

class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'pk', 'password', 'self_introduction', 'created_at']

class NovelsChildSerializer(serializers.HyperlinkedModelSerializer):
    favorite = UserChildSerializer(read_only=True, many=True)
    read_later = UserChildSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True,  many=True)
    user = UserChildSerializer(read_only=True)

    class Meta:
        model = Novel
        fields = ['pk', 'title', 'content', 'created_at', 'category', 'updated_at', 'favorite', 'read_later', 'user']

class CommentsChildSerializer(serializers.HyperlinkedModelSerializer):
    novel = NovelsChildSerializer(read_only=True)
    user = UserChildSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['title', 'content', 'created_at', 'updated_at', 'pk', 'user', 'novel']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    follow = UserChildSerializer(read_only=True,  many=True)
    comments = SerializerMethodField()
    novels = SerializerMethodField()
    follower = SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'pk', 'self_introduction', 'created_at', 'follow', 'follower', 'comments', 'novels']

    def get_comments(self, obj):
        try:
            comment_abstruct_contents = CommentsChildSerializer(Comment.objects.all().filter(user= User.objects.get(pk=obj.pk)), many=True).data
            return comment_abstruct_contents
        except Exception as e:
            print(e)
            comment_abstruct_contents = None
            return comment_abstruct_contents
    
    def get_novels(self, obj):
        try:
            novel_abstruct_contents = NovelsChildSerializer(Novel.objects.all().filter(user=User.objects.get(pk=obj.pk)), many=True).data
            return novel_abstruct_contents
        except Exception as e:
            print(e)
            novel_abstruct_contents = None
            return novel_abstruct_contents
    
    def get_follower(self, obj):
        try:
            follower = UserChildSerializer(User.objects.all().filter(follow=User.objects.get(pk=obj.pk)), many=True).data
            return follower
        except Exception as e:
            print(e)
            follower = None
            return follower

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class NovelSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True,  many=True)
    user = UserSerializer(read_only=True)
    favorite = UserSerializer(read_only=True, many=True)
    read_later = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Novel
        fields = ['pk', 'title', 'content', 'user', 'category', 'created_at', 'updated_at', 'favorite', 'favorite_num', 'read_later']

class RightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Right
        fields = ['name']

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    novel = NovelSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['user', 'novel', 'title', 'content', 'created_at', 'updated_at', 'pk']

class RightToUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RightToUser
        fields = ['right', 'user']
