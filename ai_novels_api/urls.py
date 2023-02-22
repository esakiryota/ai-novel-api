# from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

# from udemystart.urls import router as blog_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v.1.0/', include('apisite.urls')),
]