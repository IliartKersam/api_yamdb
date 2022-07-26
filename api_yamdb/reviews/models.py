import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Сategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Категория')
    slug = models.SlugField(unique=True, verbose_name='Category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField(unique=True, verbose_name='Genre')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование произведения',
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.datetime.now().year)
        ],
        verbose_name='Год издания',
        help_text="Use the following format: <YYYY>"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Сategory,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        help_text="Select a category for this title"
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр',
        help_text="Select a genre for this title"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Произведения'
        verbose_name = 'Произведение'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Название произведения'

    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments",
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments",
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата отзыва'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
