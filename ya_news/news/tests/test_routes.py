from http import HTTPStatus
from django.urls import reverse
from django.test.client import Client
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture
import pytest


def test_home_is_accessable_to_anonymous(anonymous_client: Client) -> None:
    assert anonymous_client.get(
        reverse('news:home')
    ).status_code == HTTPStatus.OK


def test_detail_is_accesable_to_anonymous(anonymous_client: Client) -> None:
    assert anonymous_client.get(
        reverse('news:detail')
    ).status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize('path', ('news:delete', 'news:edit'))
def test_comment_edit_delete_accessable_for_author(
    author_client: Client, path: str
) -> None:
    assert author_client.get(reverse(path)).status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'path, args',
    (
        ('news:edit', lazy_fixture('comment_pk')),
        ('news:delete', lazy_fixture('comment_pk')),
    ),
)
def test_redirects(anonymous_client: Client, path: str, args: tuple) -> None:
    assertRedirects(
        response=anonymous_client.get(reverse(path, args=args)),
        expected_url=reverse('login')
    )


@pytest.mark.parametrize(
        'path', ('news:home', 'news:login', 'news:logout', 'news:signup')
    )
def test_login_logout_registration_for_anonymous(
    anonymous_client: Client, path: str
) -> None:
    assert anonymous_client.get(reverse(path)).status_code == HTTPStatus.OK
