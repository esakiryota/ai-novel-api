import django_filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import UserSerializer, NovelSerializer, CategorySerializer, CommentSerializer, UserChildSerializer, LoginSerializer, RegisterSerializer
from .models import Novel, User, Category, Comment
import json
import hashlib
from django.db.models import Q
from django.db.models import Count
from django.core.mail import send_mail

@api_view(['GET', 'POST'])
def user_list(request):
    try:
        if request.method == 'GET':
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_edit(request, pk):
    try:
        data = json.loads(request.body.decode())
        user = User.objects.get(pk=pk)
        user.username = data["username"]
        user.self_introduction = data["self_introduction"]
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def user_favorites(request, pk):
    try:
        novels = Novel.objects.filter(favorite__pk=pk).all()
        serializer = NovelSerializer(novels, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def user_read_later(request, pk):
    try:
        novels = Novel.objects.filter(read_later__pk=pk).all()
        serializer = NovelSerializer(novels, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def user_follow(request, pk):
    try:
        if request.method == "GET":
            user = User.objects.get(pk=pk)
            follow = user.follow
            serializer = UserSerializer(follow, many=True)
            return Response(serializer.data)
        elif request.method == "POST":
            follow_pk = json.loads(request.body.decode())
            user = User.objects.get(pk=pk)
            to = User.objects.get(pk=follow_pk)
            user.follow.add(to)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        elif request.method == "DELETE":
            follow_pk = json.loads(request.body.decode())
            user = User.objects.get(pk=pk)
            to = User.objects.get(pk=follow_pk)
            user.follow.remove(to)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def user_follower(request, pk):
    try:
        user = User.objects.get(pk=pk)
        follower = User.objects.filter(follow__pk=user.pk).all()
        serializer = UserSerializer(follower, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def novel_list(request):
    if request.method == 'GET':
        try:
            novels = Novel.objects.order_by('created_at').all()
            serializer = NovelSerializer(novels, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        try: 
            data = json.loads(request.body.decode())
            print(data["categories"])
            user = User.objects.get(pk=data["user_id"])
            novel = Novel.objects.create(title=data["title"], content=data["content"], user=user)
            novel.save()
            for category in data["categories"]:
                category_ob = Category.objects.get(name=category)
                novel.category.add(category_ob)
            serializer = NovelSerializer(novel)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT', 'DELETE'])
def novel_detail(request, pk):
    try:
        novel = Novel.objects.get(pk=pk)
        print(novel)
    except novel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        if request.method == 'GET':
            serializer = NovelSerializer(novel)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = NovelSerializer(novel, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            novel.delete()
            return Response({"msg": "削除を完了しました"})
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def novel_search(request):
    try:
        data = json.loads(request.body.decode())
        novels = Novel.objects
        print(data)
        if data["str"] != "":
            novels = novels.filter(Q(title__contains=data["str"]) |Q(content__contains=data["str"]))

        if data["categories"]:
            novels = novels.filter(category__name__in=data["categories"]).distinct()
        
        if data["order_by"] == "created_at":
            novels = novels.order_by("created_at").reverse()
        elif data["order_by"] == "favorite":
            novels = novels.annotate(Count('favorite')).order_by('favorite__count').reverse()
        elif data["order_by"] == "read_later":
            novels = novels.annotate(Count('read_later')).order_by('read_later__count').reverse()
        novels = novels[data["page"]*10: data["page"]*10+10]
        serializer = NovelSerializer(novels, many=True)
        return  Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def novel_favorite(request):
    try:
        novels = Novel.objects.order_by('favorite_num')
        serializer = NovelSerializer(novels, many=True)
        return  Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def novel_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        novels = Novel.objects.filter(user=user).all()
        serializer = NovelSerializer(novels, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def novel_edit(request, pk):
    try:
        novel = Novel.objects.get(pk=pk);
        data = json.loads(request.body.decode())
        novel.content = data["content"]
        novel.title = data["title"]
        novel.category.clear()
        for category in data["categories"]:
            category_ob = Category.objects.get(name=category)
            novel.category.add(category_ob)
        novel.save()
        serializer = NovelSerializer(novel)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def novel_delete(request, pk):
    try:
        novel = Novel.objects.get(pk=pk).delete()
        return Response({"message": "削除完了しました"})
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def register(request):
    try:
        data = json.loads(request.body.decode())
        data["password"] = hashlib.md5(data["password"].encode()).hexdigest()
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_serializer = UserSerializer(data)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def login(request):
    try:
        data = json.loads(request.body.decode())
        user = User.objects.get(email=data["email"], password=hashlib.md5(data["password"].encode()).hexdigest())
        serializer = UserChildSerializer(user)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response({"message": "正しいメールアドレスとパスワードを入力してください。"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def category_list(request):
    try:
        categories = Category.objects.order_by('created_at').all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def novels_comment_list(request, pk):
    try:
        novel = Novel.objects.get(pk=pk)
        comments = Comment.objects.filter(novel=novel)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def profile_comment_list(request,pk):
    try:
        user = User.objects.get(pk=pk)
        comments = Comment.objects.filter(user=user).all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def comment_create(request, novel_pk, user_pk):
    try:
        data = json.loads(request.body.decode())
        novel = Novel.objects.get(pk=novel_pk)
        user = User.objects.get(pk=user_pk)
        comment = Comment(user=user, novel=novel, title=data["title"], content=data["content"])
        comment.save()
        serializer = CommentSerializer(comment)
        return  Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def comment_delete(request, novel_pk, user_pk, comment_pk):
    try:
        comment = Comment.objects.get(pk=comment_pk).delete()
        return Response({"msg" : "削除しました"})
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def comment_update(request, novel_pk, user_pk, comment_pk):
    try:
        data = json.loads(request.body.decode())
        comment = Comment.objects.get(pk=comment_pk)
        comment.title = data["title"]
        comment.content = data["content"]
        comment.save()
        serializer = CommentSerializer(comment)
        return  Response(serializer.data)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST','DELETE'])
def put_favarite(request, novel_pk, user_pk):
    try:
        if request.method == "POST":
            novel = Novel.objects.get(pk=novel_pk)
            user = User.objects.get(pk=user_pk)
            novel.favorite_num = novel.favorite_num + 1
            novel.favorite.add(user)
            novel.save()
            serializer = NovelSerializer(novel)
            return Response(serializer.data)

        if request.method == "DELETE":
            novel = Novel.objects.get(pk=novel_pk)
            user = User.objects.get(pk=user_pk)
            novel.favorite_num = novel.favorite_num - 1
            novel.favorite.remove(user)
            novel.save()
            serializer = NovelSerializer(novel)
            return Response(serializer.data)
        return Response(status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST','DELETE'])
def put_read_later(request, novel_pk, user_pk):
    try:
        if request.method == "POST":
            novel = Novel.objects.get(pk=novel_pk)
            user = User.objects.get(pk=user_pk)
            novel.read_later.add(user)

            novel.save()

            serializer = NovelSerializer(novel)

            return Response(serializer.data)

        if request.method == "DELETE":
            novel = Novel.objects.get(pk=novel_pk)
            user = User.objects.get(pk=user_pk)
            novel.read_later.remove(user)
            novel.save()
            serializer = NovelSerializer(novel)
            return Response(serializer.data)

        return Response(status.HTTP_204_NO_CONTENT)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_email(request):
    data = json.loads(request.body.decode())
    try:
        send_mail('LevoniA', data["content"],data["email"], ['esaki1217@gmail.com'], fail_silently=False)
        return Response({"msg": "送信が完了しました"})
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)





    
