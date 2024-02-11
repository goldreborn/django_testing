from django.urls import reverse
from django.test.client import Client
import pytest
from news.models import News, Comment

MAX_NEWS_PER_PAGE = 10


def test_max_news_on_main(author_client: Client) -> None:

    assert len(author_client.get(
        reverse('news:home')
    ).context['object_list']) <= MAX_NEWS_PER_PAGE


@pytest.mark.django_db
def test_news_order() -> None:

    assert News.objects.all() is not sorted


@pytest.mark.django_db
def test_comments_order() -> None:

    assert Comment.objects.all() is not sorted


@pytest.mark.django_db
def test_anonymous_has_no_comment_form(
        news_pk: tuple,
        client: Client
) -> None:
    assert 'form' not in client.get(
        reverse('news:detail', args=news_pk)
    ).context


@pytest.mark.django_db
def test_author_has_comment_form(
        news_pk: tuple,
        author_client: Client
) -> None:
    assert 'form' in author_client.get(
        reverse('news:detail', args=news_pk)
    ).context
