from datetime import datetime

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Genre, Review, Title, Сategory
from users.models import User
from . import permissions, serializers
from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Сategory.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (permissions.AdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (permissions.AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (permissions.AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers.TitleSerializer
        return serializers.OnlyReadTitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (
        permissions.IsAuthorOrAdminOrModeratorOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (
        permissions.IsAuthorOrAdminOrModeratorOrReadOnly,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=username', )
    lookup_field = 'username'
    queryset = User.objects.all()

    @action(
        methods=('GET', 'PATCH'),
        detail=False,
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            if 'role' in request.data and not request.user.is_admin:
                serializer.validated_data.pop('role')
            serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


@method_decorator(csrf_exempt)
@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = serializers.UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    user.last_login = datetime.now()
    confirmation_code = default_token_generator.make_token(user)
    email = request.data.get('email')
    send_mail(
        subject='Yamdb - confirmation code',
        message='Here is the your confirmation code:'
                f' {confirmation_code}',
        from_email='from@example.com',
        recipient_list=[email, ],
        fail_silently=False,
    )
    return Response(
        data={
            'email': serializer.validated_data['email'],
            'username': serializer.validated_data['username']
        },
        status=status.HTTP_200_OK
    )


@method_decorator(csrf_exempt)
@api_view(['POST'])
@permission_classes([AllowAny])
def get_tokens_for_user(request):
    serializer = serializers.TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    access = AccessToken.for_user(get_object_or_404(
        User, username=serializer.validated_data.get['username']))
    token = {
        'access': str(access),
    }
    return Response(token, status=status.HTTP_200_OK)
