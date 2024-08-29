from django.shortcuts import render
from posts.models import Post
from .serializers import PostSerializer

from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
    """получаем список всех постов или создаём новый пост."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
