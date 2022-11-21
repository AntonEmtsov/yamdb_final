from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api_yamdb import settings
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import username_validate

FEW_REVIEWS_ERROR = 'можно оставить только один отзыв к произведению'


class SignUpApiSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=settings.EMAIL_MAX_LENGTH,
    )
    username = serializers.CharField(
        required=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        validators=(username_validate,)
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'role',
            'email',
            'first_name',
            'last_name',
            'bio'
        ]

    def validate_username(self, value):
        username_validate(value)
        return value


class EditUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        validators=(username_validate,)
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=settings.CONFIRMATION_CODE_MAX_LENGTH,
    )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        title_id = self.context.get('view').kwargs.get('title_id')
        if (Review.objects.filter(
                title=get_object_or_404(Title, pk=title_id),
                author=self.context.get('request').user
        ).exists()):
            raise serializers.ValidationError(FEW_REVIEWS_ERROR)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleViewSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'category', 'genre', 'rating', 'description', 'year', 'name'
        )
        read_only_fields = (
            'id', 'description', 'year', 'name'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        many=False,
        required=False,
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        required='False'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'category', 'genre', 'description', 'year', 'name'
        )
