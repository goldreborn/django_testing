from http import HTTPStatus
from pytils.translit import slugify

from notes.tests.test_exampler import TestExampler
from notes.models import Note
from notes.forms import WARNING


class TestNoteLogic(TestExampler):

    def test_author_can_add_note(self):
        """Тест может ли автор добавить заметку"""
        response = self.auth_client.post(
            self.add_note_url, data=self.zametka_form
        )
        self.assertRedirects(response, expected_url=self.success_url)
        self.assertEqual(Note.objects.count(), 2)

        new_note = Note.objects.last()

        self.assertEqual(new_note.title, self.zametka_form['title'])
        self.assertEqual(new_note.text, self.zametka_form['text'])
        self.assertEqual(new_note.slug, self.zametka_form['slug'])

    def test_anonymous_cant_add_note(self):
        """Тест может ли аноним добавить заметку"""
        self.assertRedirects(
            response=self.client.post(
                self.add_note_url, data=self.zametka_form
            ),
            expected_url=f'{self.login_url}?next={self.add_note_url}'
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_slug_uniqueness(self):
        """Тест уникальности слага"""
        self.zametka_form['slug'] = self._note.slug
        response = self.auth_client.post(
            self.add_note_url, data=self.zametka_form
        )
        self.assertFormError(
            response, 'form', 'slug', errors=(self._note.slug + WARNING)
        )

        self.assertEqual(Note.objects.count(), 1)

    def test_is_slug_empty(self):
        """Тест пустой ли слаг"""
        self.zametka_form.pop('slug')

        response = self.auth_client.post(
            self.add_note_url, self.zametka_form
        )

        self.assertRedirects(response, self.success_url)

        self.assertEqual(Note.objects.count(), 2)

        new_note = Note.objects.last()

        expected_slug = slugify(self.zametka_form['title'])

        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_own_notes(self):
        """Тест автор может изменять собственные заметки"""
        self.assertRedirects(
            self.auth_client.post(
                self.edit_note_url, self.zametka_form
            ), self.success_url
        )
        self._note.refresh_from_db()

        self.assertEqual(self._note.title, self.zametka_form['title'])
        self.assertEqual(self._note.text, self.zametka_form['text'])
        self.assertEqual(self._note.slug, self.zametka_form['slug'])

    def test_author_can_delete_own_notes(self):
        """Тест автор может удалять собственные заметки"""
        self.assertRedirects(
            self.auth_client.post(
                self.delete_note_url
            ), self.success_url
        )

        self.assertEqual(Note.objects.count(), 0)

    def test_user_cant_edit_notes(self):
        """Тест может ли аноним изменять заметки"""
        self.assertEqual(
            self.reader_client.post(
                self.edit_note_url
            ).status_code,
            HTTPStatus.NOT_FOUND
        )

        note_from_db = Note.objects.get(pk=self._note.pk)

        self.assertEqual(self._note.title, note_from_db.title)
        self.assertEqual(self._note.text, note_from_db.text)
        self.assertEqual(self._note.slug, note_from_db.slug)

    def test_user_cant_delete_notes(self):
        """Тест может ли аноним удалять заметки"""
        self.assertEqual(
            self.reader_client.post(
                self.delete_note_url
            ).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(Note.objects.count(), 1)
