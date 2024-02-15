from django.contrib.auth import get_user_model

from notes.tests.test_exampler import TestExampler
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestExampler):

    def test_notes_for_author(self):
        """
        Тест присутствия заметки автора
        в контексте и object_list на странице заметок
        и отсутствия обычного пользователя
        """
        for _client, result in (
            (self.auth_client, True),
            (self.reader_client, False),
        ):
            with self.subTest(user=_client, name=result):
                self.assertIs(
                    expr1=self._note in _client.get(
                        self.notes_list_url
                    ).context.get(
                        'object_list'
                    ),
                    expr2=result
                )

    def test_add_edit_form(self):
        """
        Тест присутствия формы заметки автора в контексте и форме form
        и является ли форма классом
        """
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
