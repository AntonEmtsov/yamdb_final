import csv
import os


from pathlib import Path
from django.core.management.base import BaseCommand

from reviews.models import (
    Review, Comment, User, Title, Genre, Category, GenreTitle)

FILES = [
    ('users.csv', User),
    ('category.csv', Category),
    ('genre.csv', Genre),
    ('titles.csv', Title),
    ('review.csv', Review),
    ('comments.csv', Comment),
    ('genre_title.csv', GenreTitle),
]


class Command(BaseCommand):
    help = 'import data from csv'

    def handle(self, *args, **options):
        for file, model in FILES:
            path = Path(os.getcwd(), "static", "data", file)
            with open(path, encoding="utf8") as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    if row.get('category'):
                        row['category'] = Category.objects.get(
                            pk=row.get('category'))
                    if row.get('author'):
                        row['author'] = User.objects.get(pk=row.get('author'))
                    model(**row).save()
        print('импорт выполнен')
