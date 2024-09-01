from posts.models import Post, Group
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permission import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """получаем список всех постов или создаём новый пост."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    """получаем информацию о группе."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """получаем список комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def getting_post(self):
        return Post.objects.get(pk=self.kwargs['post_pk'])

    def get_queryset(self):
        return self.getting_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.getting_post()
        )
