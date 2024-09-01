from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from api.views import (
    PostViewSet, GroupsViewSet, CommentViewSet)


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupsViewSet)
router.register(
    r'posts/(?P<post_pk>\d+)/comments', CommentViewSet,
    basename='post-comments')

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
