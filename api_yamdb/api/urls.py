from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()

v1_router.register('categories', views.CategoryViewSet)
v1_router.register('genres', views.GenreViewSet)
v1_router.register('titles', views.TitleViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, basename='reviews'

)
v1_router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', views.get_confirmation_code),
    path('v1/auth/token/', views.get_tokens_for_user)
]
