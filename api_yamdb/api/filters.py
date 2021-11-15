from rest_framework import filters


class GenreSlugFilterBackend(filters.BaseFilterBackend):
    """
    Фильтрация по слагу жанра
    """
    def filter_queryset(self, request, queryset, view):
        genre = request.GET.get('genre')
        if genre:
            return queryset.filter(genre__slug=genre)
        return queryset


class CategorySlugFilterBackend(filters.BaseFilterBackend):
    """
    Фильтрация по слагу категории
    """
    def filter_queryset(self, request, queryset, view):
        category = request.GET.get('category')
        if category:
            return queryset.filter(category__slug=category)
        return queryset


class NameFilterBackend(filters.BaseFilterBackend):
    """
    """
    def filter_queryset(self, request, queryset, view):
        name = request.GET.get('name')
        if name:
            return queryset.filter(name__contains=name)
        return queryset


class YearFilterBackend(filters.BaseFilterBackend):
    """
    """
    def filter_queryset(self, request, queryset, view):
        year = request.GET.get('year')
        if year:
            return queryset.filter(year=year)
        return queryset
