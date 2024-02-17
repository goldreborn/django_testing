import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects
from django.utils import timezone
from http import HTTPStatus

from news.models import Comment, News
from news.forms import CommentForm
from news.forms import BAD_WORDS, WARNING

User = get_user_model()


@pytest.mark.django_db
def test_anonymous_can_not_add_comment(
        client: Client,
        news_pk: tuple
) -> None:
    """Тест аноним не может добавить комментарий"""
    test_comment = {
        'form': 'comment',
        'author': 'sdasd',
        'created': timezone.now()
    }
    client.post(
        reverse('news:detail', args=news_pk), data=test_comment
    )

    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_can_add_comment(
        author_client: Client,
        news_pk: tuple,
        comment_form: CommentForm,
        news: News,
        author: object,
) -> None:
    """Тест автор может добавить комментарий"""
    url = reverse('news:detail', args=news_pk)

    response = author_client.post(url, data=comment_form)

    assertRedirects(response, f'{url}#comments')

    assert Comment.objects.count() == 1

    comment = Comment.objects.get()

    assert comment.text == comment_form['text']
    assert comment.author == author
    assert comment.news == news


def test_if_comment_contains_bad_words(author_client: Client, news_pk) -> None:
    """Тест на плохие слова в комментарии"""
    assertFormError(
        author_client.post(
            reverse('news:detail', args=news_pk), data={
                'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
            }
        ),
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_own_comments(
        author_client: Client, comment_pk: tuple,
        comment_form: CommentForm, news_pk: tuple, comment: Comment
) -> None:
    """Тест автор может изменять свои комментарии"""
    response = author_client.post(
        reverse('news:edit', args=comment_pk), data=comment_form
    )

    url = reverse('news:detail', args=news_pk)

    assertRedirects(
        response, f'{url}#comments',
        status_code=HTTPStatus.FOUND
    )

    comment.refresh_from_db()

    assert comment.text == comment_form['text']


@pytest.mark.django_db
def test_author_can_delete_own_comments(
        author_client: Client,
        comment_pk: tuple, news_pk: tuple
) -> None:
    """Тест автор может удалять свои комментарии"""
    response = author_client.delete(
        reverse('news:delete', args=comment_pk)
    )

    url = reverse('news:detail', args=news_pk)

    assertRedirects(
        response, f'{url}#comments',
        status_code=HTTPStatus.FOUND
    )

    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_authorized_can_not_edit_other_comments(
        admin_client: Client, comment_form: CommentForm,
        comment_pk: tuple, comment: Comment
) -> None:
    """Тест автор не может изменять чужие комментарии"""
    initial_text = comment.text

    response = admin_client.post(
        reverse('news:edit', args=comment_pk), data=comment_form
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    comment.refresh_from_db()

    assert comment.text == initial_text


@pytest.mark.django_db
def test_authorized_can_not_delete_other_comments(
        admin_client: Client, comment_pk: tuple
) -> None:
    """Тест автор не может удалять чужие комментарии"""
    response = admin_client.delete(
        reverse('news:delete', args=comment_pk)
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert Comment.objects.count() == 1
