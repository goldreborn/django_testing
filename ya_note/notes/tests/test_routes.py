from http import HTTPStatus
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from notes.tests.test_exampler import TestExampler


User = get_user_model()


class TestRoutes(TestExampler):

    def test_home_page(self):
        self.assertEqual(
            self.reader_client.get(
                reverse('notes:home')
            ).status_code, HTTPStatus.OK
        )

    def test_authenticated_can_see_notes_done_add(self):
        for path in ('notes:list', 'notes:success', 'notes:add'):
            with self.subTest(user=self._author, name=path):
                self.assertEqual(
                    self.auth_client.get(
                        reverse(path)
                    ).status_code, HTTPStatus.OK
                )

    def test_access_to_detail_change_delete(self):
        for _user, status in (
            (self.auth_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND),
        ):
            for path in ('notes:detail', 'notes:edit', 'notes:delete',):
                with self.subTest(user=_user, name=path):
                    self.assertEqual(
                        _user.get(
                            reverse(path, kwargs={'slug': self._note.slug})
                        ).status_code, status
                    )

    def test_notes_paths_redirect_to_login(self):

        notes_paths = (
            'notes:success', 'notes:list', 'notes:add',
            'notes:edit', 'notes:delete', 'notes:detail'
        )

        for path in notes_paths:
            with self.subTest(name=path):
                if 'edit' in path or 'delete' in path or 'detail' in path:
                    path = reverse(path, kwargs={'slug': self._note.slug})
                else:
                    path = reverse(path)
                self.assertRedirects(
                    self.reader_client.get(path),
                    expected_url=reverse('login')
                )

    def test_registration_login_logout(self):
        for _user in (self.auth_client, self.reader_client,):
            for path in ('signup', 'login', 'logout'):
                with self.subTest(user=_user, name=path):
                    self.assertEqual(
                        _user.get(
                            reverse(path)
                        ).status_code, HTTPStatus.OK
                    )
