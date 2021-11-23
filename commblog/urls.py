"""commblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import UserCreateView, UserLoginAPIView, PostListView, PostDetailView, UserListView, UserDetailView, CommentListView, CommentDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/signup/', UserCreateView.as_view(), name='user-create'),
    path('auth/login/', UserLoginAPIView.as_view(), name="login"),
    path('auth/users/', UserListView.as_view(), name="user-list"),
    path('auth/users/<int:pk>/', UserDetailView.as_view(), name="user-detail"),
    path('posts/', PostListView.as_view(), name="post-list"),
    path('posts/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('posts/<int:pk>/comments/', CommentListView.as_view(), name="comment-list"),
    path('posts/<int:pk>/comments/<int:pk1>/', CommentDetailView.as_view(), name="comment-detail")
]
