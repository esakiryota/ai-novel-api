from django.db import models
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, unique=False, blank=False)
    password = models.TextField(max_length=100, blank=False)
    self_introduction = models.TextField(max_length=300, blank=True)
    follow = models.ManyToManyField("self", related_name="follow", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Novel(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    category = models.ManyToManyField(Category,related_name='categories', blank=True)
    favorite = models.ManyToManyField(User, related_name='users', blank=True)
    read_later = models.ManyToManyField(User, related_name='users_read_later', blank=True)
    favorite_num = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="")
    content = models.CharField(max_length=200, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Right(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RightToUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    right = models.ForeignKey(Right, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + "_" + self.right.name

