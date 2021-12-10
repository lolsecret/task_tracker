import pytest
from django.core.exceptions import ValidationError
from django.test import Client
from mixer.backend.django import mixer

from ..models import User

pytestmark = pytest.mark.django_db

class TestUserModel:
    def test_model(self):
        user = mixer.blend(User)
        assert user.pk == 1

    def test_username_case_insensitive(self):
        user = mixer.blend(User, username='lolopop12')
        assert User.objects.get(username='lOlopop12') == user

    def test_username_case_insensitive2(self):
        user = mixer.blend(User, username='lolopop12')
        assert User.objects.filter(username='lOlopop12').count() == 1

    def test_email_case_insensitive(self):
        user = mixer.blend(User, email='tamer_sabirbek@gmail.com')
        assert User.objects.get(email='Tamer_sabirbek@Gmail.com') == user

    def test_email_case_insensitive2(self):
        user = mixer.blend(User, email='tamer_sabirbek@gmail.com')
        assert User.objects.filter(email='tamer_sabirbektamer_sabirbek@Gmail.com').count() == 1

    def test_full_name(self):
        user = mixer.blend(User, first_name='Lolo', last_name='Pop')
        assert user.full_name == 'Lolo Pop'

    def test_username_regex(self):
        user = User(
            username = 'tamer_sabirbek@gmail.com',
            email = 'tamer_sabirbek@gmail.com',
            first_name = 'Lolo',
            last_name = 'Pop',
        )
        user.set_password('}P-9(e,W')
        with pytest.raises(ValidationError):
            if user.full_clean():
                user.save()
        assert User.objects.filter(username='tamer_sabirbek@gmail.com').count() == 0

class TestUserLogin:
    def test_username_case_insensitive(self):
        c = Client()
        user = mixer.blend(User, username='Lolopop12')
        user.set_password('}P-9(e,W')
        user.save()
        assert c.login(username='LoLo', password='}P-9(e,W') == True

    def test_user_can_login_with_email(self):
        c = Client()
        user = mixer.blend(User, username='lolopop12', email='tamer_sabirbek@gmail.com')
        user.set_password('}P-9(e,W')
        user.save()
        assert c.login(username='tamer_sabirbek@gmail.com', password='}P-9(e,W') == True
