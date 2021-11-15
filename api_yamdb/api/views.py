from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from reviews.models import Review, Title
from reviews.models import Genre, Category, Title
from .serializers import ReviewSerializer, CommentSerializer
from .serializers import GenreSerializer, CategorySerializer
from .serializers import TitleBaseSerializer, TitlePostSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAdminModeratorAuthorPermission, IsAdminPermission
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .filters import (GenreSlugFilterBackend, CategorySlugFilterBackend,
                      NameFilterBackend, YearFilterBackend)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self._get_title()
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        title = self._get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get('review_id'))
        )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminPermission,)

    def retrieve(self, request, slug=None):
        if not len(Genre.objects.filter(slug=slug)):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().retrieve(self, request, slug)

    def partial_update(self, request, slug=None):
        if not len(Genre.objects.filter(slug=slug)):
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().retrieve(self, request, slug)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminPermission,)

    def retrieve(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (NameFilterBackend, GenreSlugFilterBackend,
                       CategorySlugFilterBackend, YearFilterBackend)
    permission_classes = (IsAdminPermission, IsAuthenticatedOrReadOnly)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitlePostSerializer
        return TitleBaseSerializer
