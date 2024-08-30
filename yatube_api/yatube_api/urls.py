from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from api.views import (
    PostViewSet, GroupsViewSet, GroupViewSet, PostsCommentViewSet, CommentViewSet
)

router = DefaultRouter()
URL_API = 'api/v1/'
router.register(URL_API + 'posts', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{URL_API}api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
    path(f'{URL_API}groups/', GroupsViewSet.as_view()),
    path(f'{URL_API}groups/<int:pk>/', GroupViewSet.as_view()),
    path(f'{URL_API}posts/<int:pk>/comments/', PostsCommentViewSet.as_view()),
    path(
        f'{URL_API}posts/<int:pk>/comments/<int:pk_comment>/',
        CommentViewSet.as_view()
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
