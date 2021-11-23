from django.contrib.auth.models import User

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token

from api.serializers import UserSerializer, UserLoginSerializer, PostSerializer, CommentSerializer
from api.models import Post, Comment
from api.permissions import IsOwnerOrReadOnly

# USER VIEWS
class UserCreateView(APIView):
    
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(
                    {
                        "message": "Signup successful!",
                        "data": json
                    }
                    # json, status=status.HTTP_201_CREATED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):

    permission_classes = (permissions.AllowAny, )
    # permission_classes = [permissions.AllowAny, permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            json = serializer.data
            return Response({
                        "message": "Login successful!",
                        "data": json
                    })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# POST VIEWS

class PostListView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# COMMENT VIEWS
class CommentListView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_crate(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
