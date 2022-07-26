from django.contrib import admin

from .models import Comment, Genre, Review, Title, Сategory


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'list_display_genre',
    )
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'

    def list_display_genre(self, obj):
        return ', '.join(genre.name for genre in obj.genre.all())

    list_display_genre.short_description = 'Genre'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', )
    search_fields = ('name',)
    list_filter = ('slug',)


class СategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', )
    search_fields = ('name',)
    list_filter = ('slug',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'score', 'pub_date', 'title')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date')
    search_fields = ('text', 'author',)
    list_filter = ('text', 'author', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Сategory, СategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
