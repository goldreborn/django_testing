from http import HTTPStatus
from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.tests.test_exampler import TestExampler
from notes.models import Note


User = get_user_model()


class TestNoteLogic(TestExampler):

    zametka_form = {
        'title': 'Zametka',
        'text': 'zametka text',
        'slug': 'zametka_slug'
    }

    def test_author_can_add_note(self):
        """Тест может ли автор добавить заметку"""
        self.assertRedirects(
            self.auth_client.get(
                self.success_url, data=self.zametka_form
            )
        )
        self.assertEqual(Note.objects.count(), 1)

        new_note = Note.objects.get()

        self.assertEqual(new_note.title, self.zametka_form['title'])
        self.assertEqual(new_note.text, self.zametka_form['text'])
        self.assertEqual(new_note.slug, self.zametka_form['slug'])
        self.assertIs(new_note.author, self._author)

    def test_anonymous_can_add_note(self):
        """Тест может ли аноним добавить заметку"""
        self.assertRedirects(
            self.reader_client.post(
                self.add_note_url, data=self.zametka_form
            ),
            f'{self.login_url}?next={self.add_note_url}'
        )
        self.assertEqual(
            Note.objects.count(), 0
        )

    def test_slug_uniqueness(self):
        """Тест уникальности слага"""
        self.zametka_form['slug'] = self._note.slug

        self.assertFormError(
            self.auth_client.post(
                self.add_note_url, data=self.zametka_form
            ),
            'form', 'slug', errors=(
                self._note.slug + Warning(
                    'Found not unique slug'
                )
            )
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_is_slug_empty(self):
        """Тест пустой ли слаг"""
        self.assertRedirects(
            self.auth_client.post(
                self.add_note_url, data=self.zametka_form
            ), self.add_note_url
        )
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(
            Note.objects.get().slug, slugify(self.zametka_form['title'])
        )

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
        self._note.slug, self.zametka_form['slug']

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
