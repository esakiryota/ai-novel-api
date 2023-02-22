from django.contrib import admin
from .models import Category, Novel, Right, Comment, RightToUser, User

admin.site.register(Category)
admin.site.register(Novel)
admin.site.register(Right)
admin.site.register(Comment)
admin.site.register(RightToUser)
admin.site.register(User)

# Register your models here.
