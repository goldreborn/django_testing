from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
import pytest

from news.models import Comment
from news.forms import CommentForm

User = get_user_model()

test_comment = {'form': 'comment'}

BAD_WORDS = ('Какашка', 'Хулиган',)


def test_anonymous_can_not_add_comment(
        client: Client,
        news_pk: tuple
) -> None:
    client.post(
        reverse('news:detail', args=news_pk), data=test_comment
    )

    assert Comment.objects.count() == 0


def test_authenticated_can_add_comment(
        author_client: Client,
        news_pk: tuple
) -> None:
    author_client.post(reverse('news:detail', args=news_pk), data=test_comment)

    assert Comment.objects.count != 0


def test_if_comment_contains_bad_words() -> None:
    assert not any([x == test_comment['form'] for x in BAD_WORDS])


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    'path, args',
    (
        ('news:edit', lazy_fixture('comment_pk')),
        ('news:delete', lazy_fixture('comment_pk')),
    ),
)
def test_author_can_edit_delete_own_comments(
        author_client: Client, path: str, args: tuple,
        comment_form: CommentForm
) -> None:
    assert author_client.post(
        reverse(path, args=args), data=comment_form
    ).status_code == 302


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    'path, args',
    (
        ('news:edit', lazy_fixture('comment_pk')),
        ('news:delete', lazy_fixture('comment_pk')),
    ),
)
def test_author_can_not_edit_delete_other_comments(
        author_client: Client, path: str, args: tuple,
        comment_form: CommentForm
) -> None:
    assert author_client.post(
        reverse(path, args=args), data=comment_form
    ).status_code == 302
