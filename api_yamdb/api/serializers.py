from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Genre, Review, Title, User, Сategory


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio'
        )
        model = User


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('review',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('title', 'author')
        model = Review

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = request.parser_context['kwargs'].get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(
                    title=title,
                    author=request.user).exists():
                raise ValidationError('Нельзя добавить второй отзыв'
                                      ' на то же самое произведение')
        return data


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=100)

    def validate(self, data):
        if not default_token_generator.check_token(
            get_object_or_404(User, username=data['username']),
            data['confirmation_code']
        ):
            raise serializers.ValidationError('Invalid confirmation code!')
        return True

    class Meta:
        fields = (
            'username',
            'confirmation_code'
        )
        model = User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Сategory
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Сategory.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')


class OnlyReadTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category',)
