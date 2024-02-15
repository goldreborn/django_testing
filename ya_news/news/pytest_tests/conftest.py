import pytest
from django.test.client import Client

from datetime import datetime

from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from news.models import News, Comment


@pytest.fixture
def author(django_user_model) -> object:
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def news() -> News:
    return News.objects.create(
        title='Где свет?!',
        text='Абэма продолжает выкручивать лампочки в подъезде',
        date=datetime.today()
    )


@pytest.fixture
def create_news() -> None:
    News.objects.bulk_create(
        News(title=f'Новость {index}', text='Просто текст.')
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def create_comments() -> None:
    Comment.objects.bulk_create(
        Comment(title=f'Комментарий {index}', text='Просто комментарий.')
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )


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
        'text': 'текст'
    }


@pytest.fixture
def news_pk(news: News) -> tuple:
    return (news.pk,)


@pytest.fixture
def comment_pk(comment: Comment) -> tuple:
    return (comment.pk,)
