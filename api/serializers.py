from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Q
from api.models import Post, Comment


# POST SERIALIZER
class PostSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'comments']


# COMMENT SERIALIZER
class CommentSerializer(serializers.ModelSerializer):
    #author = serializers.ReadOnlyField(source='author.username')
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='id', write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post']


# USER SERIALIZERS
class UserSerializer(serializers.ModelSerializer):

    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'posts', 'comments']


class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        write_only=True,
        label="Email Address"
    )

    token = serializers.CharField(
        allow_blank=True,
        read_only=True
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta(object):
        model = User
        fields = ['email', 'password', 'token']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if not email:
            raise serializers.ValidationError("Please enter username or email to login.")

        user = User.objects.filter(
            Q(email=email)
        ).exclude(
            email__isnull=True
        ).exclude(
            email__iexact=''
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            token, created = Token.objects.get_or_create(user=user_obj)
            data['token'] = token
        else:
            raise serializers.ValidationError("User not active.")

        return data
