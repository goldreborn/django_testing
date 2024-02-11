from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.tests.test_exampler import TestExampler

User = get_user_model()


class TestContent(TestExampler):

    def test_note_passes_throw_object_list_and_context(self):

        self.assertIn(
            self._note,
            self.auth_client.get(
                reverse('notes:list')
            ).context['object_list']
        )

    def test_users_notes_not_in_other_users_notes(self):

        self.assertNotIn(
            self._note, self.auth_client.get(
                reverse('notes:list')
            ).context.pop()
        )

    def test_add_edit_form(self):

        for path in ('notes:add', 'notes:edit',):
            self.assertIn(
                'form', self.auth_client.get(
                    reverse(path, kwargs={
                        'slug': self._note.slug
                    } if path == 'notes:edit' else None)
                ).context
            )
