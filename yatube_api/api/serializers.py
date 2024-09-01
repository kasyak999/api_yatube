from rest_framework import serializers
from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    pub_date = serializers.DateTimeField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    group = serializers.SlugRelatedField(
        slug_field='title', read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'

    def get_comments(self, obj):
        return obj.comments.count()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    # post = PostSerializer(required=False)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created', 'post')
