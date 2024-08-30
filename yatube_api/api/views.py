from django.shortcuts import render
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, PostsCommentSerializer

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PostViewSet(viewsets.ModelViewSet):
    """получаем список всех постов или создаём новый пост."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupsViewSet(APIView):
    """получаем список всех групп."""
    def get(self, request):
        group = Group.objects.all()
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)


class GroupViewSet(APIView):
    """получаем информацию о группе с идентификатором."""
    def get(self, request, pk):
        group = Group.objects.get(pk=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)


class PostsCommentViewSet(APIView):
    """получаем список всех комментариев поста с идентификатором"""
    def get(self, request, pk):
        comment = Comment.objects.filter(post=pk)
        serializer = PostsCommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = PostsCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                post=Post.objects.get(pk=pk)
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
