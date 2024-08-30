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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(APIView):
    def get(self, request, pk, pk_comment):
        comment = Comment.objects.get(pk=pk_comment)
        serializer = PostsCommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, pk_comment):
        comment = Comment.objects.get(pk=pk_comment)
        serializer = PostsCommentSerializer(
            comment, data=request.data
        )
        if comment.author == self.request.user:
            if serializer.is_valid():
                serializer.save(
                    author=self.request.user,
                    post=Post.objects.get(pk=pk)
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk, pk_comment):
        comment = Comment.objects.get(pk=pk_comment)
        serializer = PostsCommentSerializer(
            comment, data=request.data, partial=True)
        if comment.author == self.request.user:
            if serializer.is_valid():
                serializer.save(
                    author=self.request.user,
                    post=Post.objects.get(pk=pk)
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, pk_comment):
        comment = Comment.objects.get(pk=pk_comment)
        if comment.author == self.request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
