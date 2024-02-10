from django.test.client import Client
import pytest
from datetime import datetime

from news.models import News, Comment


@pytest.fixture
def author(django_user_model) -> object:
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def anonymous(django_user_model) -> object:
    return django_user_model.objects.create(username='Анон')


@pytest.fixture
def author_client(author: Client) -> None:
    return Client().force_login(author)


@pytest.fixture
def anonymous_client(anonymous: Client) -> None:
    return Client().force_login(anonymous)


@pytest.fixture
def news() -> News:
    return News.objects.create(
        title='Где свет?!',
        text='Абэма продолжает выкручивать лампочки в подъезде',
        pub_date=datetime.today()
    )


@pytest.fixture
def news_form() -> dict:
    return {
        'title': 'заголовок',
        'text': 'текст',
        'date': 'дата'
    }


@pytest.fixture
def comment(news: News, author: Client) -> Comment:
    return Comment.objects.create(
        news=news,
        author=author,
        text='Поймайте его!',
        created=datetime.today()
    )


@pytest.fixture
def comment_form(news: News) -> dict:
    return {
        'news': news,
        'author': 'автор',
        'text': 'текст',
        'created': datetime.today()
    }


@pytest.fixture
def news_pk(news: News) -> tuple:
    return (news.pk,)


@pytest.fixture
def comment_pk(comment: Comment) -> tuple:
    return (comment.pk,)
