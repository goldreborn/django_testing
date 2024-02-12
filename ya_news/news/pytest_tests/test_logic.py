import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertFormError
from news.models import Comment
from news.forms import CommentForm

from news.forms import BAD_WORDS, WARNING

User = get_user_model()

test_comment = {'form': 'comment'}


@pytest.mark.django_db
def test_anonymous_can_not_add_comment(
        client: Client,
        news_pk: tuple
) -> None:
    """Тест аноним не может добавить комментарий"""
    client.post(
        reverse('news:detail', args=news_pk), data=test_comment
    )

    assert Comment.objects.count() == 0


def test_authenticated_can_add_comment(
        author_client: Client,
        news_pk: tuple
) -> None:
    """Тест автор может добавить комментарий"""
    author_client.post(reverse('news:detail', args=news_pk), data=test_comment)

    new_comment = Comment.objects.get()
    new_comment.refresh_from_db()

    assert Comment.objects.count == 1
    assert new_comment.news.pk == news_pk
    assert new_comment.text == test_comment['form']


def test_if_comment_contains_bad_words(author_client: Client) -> None:
    """Тест на плохие слова в комментарии"""
    assertFormError(
        author_client.post(
            reverse('news:add'), data={
                'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
            }
        ),
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
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
    """Тест автор может изменять, удалять свои комментарии"""
    assert author_client.post(
        reverse(path, args=args), data=comment_form
    ).status_code == 302


@pytest.mark.django_db
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
    """Тест автор не может удалять, изменять чужие комментарии"""
    assert author_client.post(
        reverse(path, args=args), data=comment_form
    ).status_code == 302
