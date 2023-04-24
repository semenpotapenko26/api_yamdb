from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import TEXT_COMMENT


class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Название категории")
    slug = models.SlugField(unique=True, help_text="Slug категории")

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Название жанра")
    slug = models.SlugField(unique=True, help_text="Slug жанра")

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, help_text="Название произведения")
    year = models.IntegerField(help_text="Год создания")
    description = models.TextField(help_text="Описание")
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='titles'
                                 )
    genre = models.ManyToManyField(Genre, through="Genre_Title")

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              )
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(help_text="Текст отзыва")
    score = models.PositiveSmallIntegerField(
        help_text="Рейтинг",
        validators=[
            MinValueValidator(1, 'Минимально 1'),
            MaxValueValidator(10, 'Максимально 10')],)
    pub_date = models.DateTimeField(
        help_text="Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ['title', 'author']

    def __str__(self):
        return self.text[:TEXT_COMMENT]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_COMMENT]
