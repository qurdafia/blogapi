from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import datetime

# Create your models here.
class Post(models.Model):
    created = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True, default='')
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title

class Comment(models.Model):
    created = models.DateTimeField(default=datetime.datetime.now)
    content = models.TextField(blank=False)
    author = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.content