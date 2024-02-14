from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestExampler(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls._author = User.objects.create(username='Шрэк')
        cls._reader = User.objects.create(username='Осёл')
        cls._note = Note.objects.create(
            title='Освобождение Фионы',
            text='Залезть в башню, найти принцессу и победить дракона',
            author=cls._author
        )
        cls.auth_client = Client()
        cls.auth_client.force_login(cls._author)

        cls.reader_client = Client()
        cls.reader_client.force_login(cls._reader)

        cls.home_url = reverse('notes:home')
        cls.login_url = reverse('users:login')
        cls.signup_url = reverse('users:signup')
        cls.logout_url = reverse('users:logout')
        cls.add_note_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.delete_note_url = reverse(
            'notes:delete', kwargs={'slug': cls._note.slug}
        )
        cls.edit_note_url = reverse(
            'notes:edit', kwargs={'slug': cls._note.slug}
        )
        cls.notes_list_url = reverse('notes:list')
        cls.note_detail_url = reverse(
            'notes:detail', kwargs={'slug': cls._note.slug}
        )
        cls.zametka_form = {
            'title': 'Zametka_title',
            'text': 'Zametka_text',
            'slug': 'slugger'
        }
