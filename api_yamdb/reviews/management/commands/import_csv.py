import pandas as pd
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Genre_Title, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Импорт данных из CSV в бд'

    def handle(self, *args, **options):
        '''Users'''
        df = pd.read_csv("static/data/users.csv")
        for (import_id,
             import_username,
             import_email,
             import_role,
             import_bio,
             import_first_name,
             import_last_name) in zip(
            df.id,
            df.username,
            df.email,
            df.role,
            df.bio,
            df.first_name,
            df.last_name
        ):
            models = User(id=import_id,
                          username=import_username,
                          email=import_email,
                          role=import_role,
                          bio=import_bio,
                          first_name=import_first_name,
                          last_name=import_last_name
                          )
            models.save()

        '''Category'''
        df = pd.read_csv("static/data/category.csv")
        for import_name, import_slug in zip(df.name, df.slug):
            models = Category(name=import_name, slug=import_slug)
            models.save()

        '''Title'''
        df = pd.read_csv("static/data/titles.csv")
        for import_name, import_year, import_category in zip(
            df.name, df.year, df.category
        ):
            models = Title(name=import_name,
                           year=import_year,
                           category=Category(import_category))
            models.save()

        '''Reviews'''
        df = pd.read_csv("static/data/review.csv")
        for (import_title_id,
             import_text,
             import_author,
             import_score,
             import_pub_date) in zip(
            df.title_id,
            df.text,
            df.author,
            df.score,
            df.pub_date
        ):
            models = Review(
                title_id=import_title_id,
                text=import_text,
                author=User(import_author),
                score=import_score,
                pub_date=import_pub_date
            )
            models.save()

        '''Comments'''
        df = pd.read_csv("static/data/comments.csv")
        for (import_review_id,
             import_text,
             import_author,
             import_pub_date) in zip(df.review_id,
                                     df.text,
                                     df.author,
                                     df.pub_date
                                     ):
            models = Comment(review_id=import_review_id,
                             text=import_text,
                             author=User(import_author),
                             pub_date=import_pub_date)
            models.save()

        '''Genre'''
        df = pd.read_csv("static/data/genre.csv")
        for import_name, import_slug in zip(
            df.name, df.slug
        ):
            models = Genre(name=import_name,
                           slug=import_slug)
            models.save()

        '''Genre_title'''
        df = pd.read_csv("static/data/genre_title.csv")
        for import_title_id, import_genre_id in zip(
            df.title_id, df.genre_id
        ):
            models = Genre_Title(
                title_id=import_title_id,
                genre_id=import_genre_id
            )
            models.save()
