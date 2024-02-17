import pytest
from django.urls import reverse
from django.test.client import Client
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture
from http import HTTPStatus


@pytest.mark.django_db
@pytest.mark.parametrize(
    'path, args',
    (
        ('news:edit', lazy_fixture('comment_pk')),
        ('news:delete', lazy_fixture('comment_pk')),
    ),
)
@pytest.mark.parametrize(
    'user_type, status',
    (
        (
            (lazy_fixture('author_client'), HTTPStatus.OK),
            (lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND)
        )
    )
)
def test_comment_edit_delete_access_for_authorized_user(
    path: str, args: tuple,
    user_type: Client, status: HTTPStatus
) -> None:
    """
    Тест доступности удаления и изменения комментария
    для авторизованного клиента
    """
    assert user_type.get(
        reverse(path, args=args)
    ).status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'path, args',
    (
        ('news:edit', lazy_fixture('comment_pk')),
        ('news:delete', lazy_fixture('comment_pk')),
    ),
)
def test_redirects(client: Client, path: str, args: tuple) -> None:
    """Тест редиректов"""
    url = reverse(path, args=args)

    assertRedirects(
        client.get(url), expected_url='{x}?next={y}'.format(
            x=reverse('users:login'), y=url
        )
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'path, args',
    (
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', lazy_fixture('news_pk')),
        ('news:home', None),
    )
)
def test_login_logout_registration_for_anonymous(
    client: Client, path: str, args: tuple
) -> None:
    """Тест регистрации, логина, логаута для анонима"""
    assert client.get(
        reverse(path, args=args)
    ).status_code == HTTPStatus.OK
