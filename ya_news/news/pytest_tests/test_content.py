import pytest
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from django.urls import reverse
from django.test.client import Client

from news.forms import CommentForm


def test_max_news_on_main(author_client: Client) -> None:
    """Тест количества новостей на главной странице"""
    assert len(author_client.get(
        reverse('news:home')
    ).context.get(key='object_list')) <= NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client):
    all_dates = [
        news.date for news in client.get(
            reverse('news:home')
        ).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.django_db
def test_comments_order(client, news_pk):

    response = client.get(reverse('news:detail', args=news_pk))

    assert 'news' in response.context

    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)

    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_has_no_comment_form(
        news_pk: tuple,
        client: Client
) -> None:
    """Тест аноним не имеет формы"""
    assert 'form' not in client.get(
        reverse('news:detail', args=news_pk)
    ).context


@pytest.mark.django_db
def test_author_has_comment_form(
        news_pk: tuple,
        author_client: Client
) -> None:
    """Тест автор имеет форму"""
    response = author_client.get(reverse('news:detail', args=news_pk))

    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
