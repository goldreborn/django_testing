from django.urls import reverse
from django.test.client import Client

from news.models import News, Comment

MAX_NEWS_PER_PAGE = 10


def test_max_news_on_main(author_client: Client) -> None:

    assert len(author_client.get(
        reverse('news:home')
    ).context['object_list']) <= MAX_NEWS_PER_PAGE


def test_news_order(news: News) -> None:

    assert news.objects is sorted


def test_comments_order(news_pk: tuple, comments: Comment) -> None:

    assert comments.objects.filter(news__pk=news_pk) is sorted


def test_anonymous_has_no_comment_form(
        news_pk: tuple,
        comment_pk: tuple,
        anonymous_client: Client
) -> None:

    assert 'form' not in anonymous_client.get(
        reverse('news:add', args=(news_pk, comment_pk))
    ).context


def test_author_has_comment_form(
        news_pk: tuple,
        comment_pk: tuple,
        author_client: Client
) -> None:

    assert 'form' in author_client.get(
        reverse('news:add', args=(news_pk, comment_pk))
    ).context
