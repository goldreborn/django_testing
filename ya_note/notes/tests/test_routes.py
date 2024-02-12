from http import HTTPStatus
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.tests.test_exampler import TestExampler


User = get_user_model()


class TestRoutes(TestExampler):

    def test_home_page(self):
        """Тест домашней страницы"""
        self.assertEqual(
            self.reader_client.get(
                reverse('notes:home')
            ).status_code, HTTPStatus.OK
        )

    def test_authenticated_can_see_notes_done_add(self):
        """Тест доступа заметок, удачной страницы, добавления заметки"""
        for path in (
            self.notes_list_url, self.success_url, self.add_note_url,
        ):
            with self.subTest(user=self._author, name=path):
                self.assertEqual(
                    self.auth_client.get(
                        path
                    ).status_code, HTTPStatus.OK
                )

    def test_access_to_detail_change_delete(self):
        """Тест доступа к детальной заметке, изменению или удалению"""
        for _user, status in (
            (self.auth_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND),
        ):
            for path in (
                self.note_detail_url, self.edit_note_url, self.delete_note_url,
            ):
                with self.subTest(user=_user, name=path):
                    self.assertEqual(
                        _user.get(
                            path
                        ).status_code, status
                    )

    def test_notes_paths_redirect_to_login(self):
        """Тест редиректа на логин"""
        notes_paths = (
            self.success_url, self.notes_list_url, self.add_note_url,
            self.edit_note_url, self.delete_note_url, self.note_detail_url,
        )

        for path in notes_paths:
            with self.subTest(name=path):
                self.assertRedirects(
                    self.client.get(path),
                    expected_url='{x}?next={y}'.format(
                        x=reverse('users:login'), y=path
                    )
                )

    def test_registration_login_logout(self):
        """Тест доступности страниц регистрации, логина, логаута для всех"""
        for _user in (self.auth_client, self.reader_client,):
            for path in (
                self.login_url, self.logout_url, self.signup_url
            ):
                with self.subTest(user=_user, name=path):
                    self.assertEqual(
                        _user.get(
                            path
                        ).status_code, HTTPStatus.OK
                    )
