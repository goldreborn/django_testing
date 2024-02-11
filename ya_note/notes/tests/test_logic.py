from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from pytils.translit import slugify

from notes.tests.test_exampler import TestExampler
from notes.models import Note


User = get_user_model()


class TestNoteAdd(TestExampler):

    zametka_form = {'form': 'Zametka'}

    def test_authorized_user_can_create_notes(self):
        self.auth_client.post(
            path=reverse('notes:add'), data=self.zametka_form
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_anonymous_user_cant_create_notes(self):
        self.reader_client.post(
            path=reverse('notes:add'), data=self.zametka_form
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_create_slug_if_note_does_not_has_slug(self):

        if self._note.slug is None:
            self._note.slug = slugify(self._note.text)

    def test_cannot_create_identical_slugs(self):
        self.assertNotIn(self._note.slug, Note.objects.values(
            'slug'
        ))


class TestNoteEdit(TestExampler):

    note_text_example = 'шРоОоК!'

    def test_author_or_anonymous_can_edit_comments(self):

        for _user, status in (
            (self.auth_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND)
        ):
            self.assertEqual(
                _user.post(
                    reverse(
                        'notes:edit', kwargs={
                            'slug': self._note.slug
                        }
                    ), data={
                        'text': self.note_text_example
                    }
                ).status_code, status
            )
            self._note.refresh_from_db()


class TestNoteDelete(TestExampler):

    def test_author_can_delete_own_note(self):

        self.assertRedirects(
            self.auth_client.delete(
                self.delete_note_url
            ), expected_url=reverse('notes:success')
        )
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cant_delete_other_users_notes(self):

        self.assertEqual(
            self.reader_client.delete(self.delete_note_url).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(Note.objects.count(), 1)
