from django.contrib import admin

from .models import Title, User, Genre, Category, Comment, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'text', 'pub_date',)
    search_fields = ('author', 'text',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'year', 'description',)
    search_fields = ('name', 'year', 'category',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'text', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'username', 'email',)
    search_fields = ('username', 'role',)
    list_filter = ('role', 'is_superuser',)
    empty_value_display = '-пусто-'
