from django.db import models
from users.models import User
from .validators import my_year_validator
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        unique=True,
    )

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    year = models.PositiveSmallIntegerField(
        validators=[my_year_validator],
        verbose_name='Дата выхода',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta():
        verbose_name = 'title'
        verbose_name_plural = 'titles'


class Review(models.Model):
    SCORE_CHOICES = [(i, i) for i in range(1, 11)]
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ('-pub_date',)

        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'), name='unique_relations'),
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
