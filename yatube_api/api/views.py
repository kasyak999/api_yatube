from posts.models import Post, Group, Comment
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer)
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class PostViewSet(viewsets.ModelViewSet):
    """получаем список всех постов или создаём новый пост."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, partial=True, pk=None):
        post = self.get_object()
        if post.author == self.request.user:
            return super().update(request, pk)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, partial=True, pk=None):
        post = self.get_object()
        if post.author == self.request.user:
            return super().partial_update(request, pk)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk):
        post = self.get_object()
        if post.author == self.request.user:
            return super().destroy(request, pk)
        return Response(status=status.HTTP_403_FORBIDDEN)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    """получаем информацию о группе."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostsCommentViewSet(viewsets.ModelViewSet):
    """получаем список всех комментариев."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(pk=self.kwargs['post_pk']))

    def update(self, request, post_pk, pk=None):
        comment = self.get_object()
        if comment.author == self.request.user:
            return super().update(request, pk)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, post_pk, pk=None):
        comment = self.get_object()
        if comment.author == self.request.user:
            return super().partial_update(request, pk)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, post_pk, pk):
        comment = self.get_object()
        if comment.author == self.request.user:
            return super().destroy(request, pk)
        return Response(status=status.HTTP_403_FORBIDDEN)
