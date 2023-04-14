import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'rating', 'description', 'genre', 'category')


class TitlePostSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug',
                                many=False,
                                queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug', many=True,
                             queryset=Genre.objects.all())
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        serializer = TitleGetSerializer(instance)
        return serializer.data

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                f'Сейчас {year} год. Назад в будущее!!!')
        return value
