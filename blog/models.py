from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_comments"
    )
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
