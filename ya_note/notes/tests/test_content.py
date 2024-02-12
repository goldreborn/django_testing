from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.tests.test_exampler import TestExampler
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestExampler):

    def test_notes_for_author(self):
        """Тест заметка в object_list"""
        for _client, result in (
            (self.auth_client, True),
            (self.reader_client, False),
        ):
            with self.subTest(user=_client, name=result):
                self.assertIs(
                    expr1=self._note in _client.get(
                        self.notes_list_url
                    ).context[
                        'object_list'
                    ],
                    expr2=result
                )

    def test_add_edit_form(self):
        """Тест формы"""
        for path in (
            self.add_note_url, self.edit_note_url,
        ):
            with self.subTest(name=path):

                context = self.auth_client.get(path).context

                self.assertIn(
                    'form',
                    context
                )
                self.assertIsInstance(
                    context['form'], NoteForm
                )
