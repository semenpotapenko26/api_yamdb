from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
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
                              on_delete=models.SET_NULL,
                              null=True,
                              )
    genre = models.ForeignKey(Genre,
                              on_delete=models.SET_NULL,
                              null=True,
                              )
