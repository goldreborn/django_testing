from http import HTTPStatus
from django.urls import reverse
from django.test.client import Client
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture
import pytest


@pytest.mark.django_db
def test_home_is_accessable_to_anonymous(client: Client) -> None:
    assert client.get(
        reverse('news:home')
    ).status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_is_accesable_to_anonymous(
        client: Client,
        news_pk: tuple
) -> None:
    assert client.get(
        reverse('news:detail', args=news_pk)
    ).status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'path, args',
    (
        ('news:edit', lazy_fixture('comment_pk')),
        ('news:delete', lazy_fixture('comment_pk')),
    ),
)
def test_comment_edit_delete_accessable_for_author(
    author_client: Client, path: str, args: tuple
) -> None:
    assert author_client.get(
        reverse(path, args=args)
    ).status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'path, args',
    (
        ('news:edit', lazy_fixture('comment_pk')),
        ('news:delete', lazy_fixture('comment_pk')),
    ),
)
def test_redirects(client: Client, path: str, args: tuple) -> None:
    if args is not None:
        url = f'{reverse(path, args=args)}'
    else:
        url = reverse(path)

    assertRedirects(
        client.get(url), expected_url='{x}?next={y}'.format(
            x=reverse('users:login'), y=url
        )
    )


@pytest.mark.parametrize(
    'path', ('users:login', 'users:logout', 'users:signup')
)
def test_login_logout_registration_for_anonymous(
    client: Client, path: str
) -> None:
    assert client.get(
        reverse(path)
    ).status_code == HTTPStatus.OK
