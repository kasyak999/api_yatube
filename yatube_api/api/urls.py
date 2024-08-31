from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from api.views import (
    PostViewSet, GroupsViewSet, PostsCommentViewSet)


router = DefaultRouter()
# URL_API = 'v1/'
router.register('v1/posts', PostViewSet)
router.register('v1/groups', GroupsViewSet)
router.register(
    r'v1/posts/(?P<post_pk>\d+)/comments', PostsCommentViewSet,
    basename='post-comments')

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
