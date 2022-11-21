from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from api_yamdb.settings import DEFAULT_EMAIL

from .filters import Filter
from .permissions import IsAdmin, IsAuthorOrStaffOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          EditUserSerializer, GenreSerializer,
                          ReviewSerializer, SignUpApiSerializer,
                          TitleViewSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaffOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(
            Review,
            title=get_object_or_404(Title, pk=self.kwargs.get('title_id')),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class SignUpApi(APIView):
    permission_classes = (AllowAny,)

    def send_email(self, email, user, message):
        send_mail(
            subject='Вы зарегистрировались на сервисе YAMDB.',
            message=(
                f'{message} '
                f'Ваш код: {default_token_generator.make_token(user)}'
            ),
            from_email=DEFAULT_EMAIL,
            recipient_list=[email],
        )

    def post(self, request):
        serializer = SignUpApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
            )
        except IntegrityError:
            return Response(
                'Пользователь с таким email или именем '
                'пользователя уже зарегистрирован',
                status=status.HTTP_400_BAD_REQUEST
            )
        self.send_email(user.email, user, 'Спасибо за регистрацию.')
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenApi(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.data.get('username')
        )
        if default_token_generator.check_token(
            user, serializer.data.get('confirmation_code')
        ):
            return Response(
                {'Токен': str(RefreshToken.for_user(user))},
                status=status.HTTP_200_OK
            )
        return Response('Неверный код.', status=status.HTTP_400_BAD_REQUEST)


class UsersApiViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrStaffOrReadOnly, IsAdmin)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['username', ]
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
        detail=False,
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if not request.method == 'PATCH':
            return Response(
                self.get_serializer(user).data,
                status=status.HTTP_200_OK,
            )
        serializer = EditUserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (ReadOnly | IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    serializer_class = TitleWriteSerializer
    permission_classes = (ReadOnly | IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = Filter
    ordering_fields = '_all_'
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleViewSerializer
        return TitleWriteSerializer
