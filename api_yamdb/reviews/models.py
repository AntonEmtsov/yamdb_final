from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb import settings

from .validators import username_validate, validate_year

USER = 'user'
MODERATOR = 'moderator'
ADMINISTRATOR = 'admin'
ROLES = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMINISTRATOR, 'Администратор'),
]
FEW_REVIEWS_ERROR = 'можно оставить только один отзыв к произведению'


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        validators=[username_validate],
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.FIRST_NAME_MAX_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.LAST_NAME_MAX_LENGTH,
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == ADMINISTRATOR or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class BaseCategoryGenre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name[:15]


class Category(BaseCategoryGenre):

    class Meta(BaseCategoryGenre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseCategoryGenre):

    class Meta(BaseCategoryGenre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(verbose_name='Название')
    year = models.IntegerField(
        validators=[validate_year], verbose_name='Год выпуска')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category',
        verbose_name='Категория',
        help_text='Категория, к которой будет относиться произведение'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        verbose_name='Жанр',
        through='GenreTitle',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


class AbstractReviewComment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='автор'
    )
    text = models.TextField('текст')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    FOR_STR = '{model}: {author}. {text:.30}'

    class Meta:
        abstract = True
        default_related_name = '%(class)ss'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.FOR_STR.format(
            model=self.__class__.__name__,
            author=self.author.username,
            text=self.text
        )


class Review(AbstractReviewComment):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение'
    )
    score = models.IntegerField(
        'оценка', choices=[(i, str(i)) for i in range(1, 11)]
    )

    class Meta(AbstractReviewComment.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name=FEW_REVIEWS_ERROR),
        ]


class Comment(AbstractReviewComment):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='отзыв')

    class Meta(AbstractReviewComment.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} - {self.title}'
