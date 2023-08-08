from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='aslava@mail.ru',
            is_superuser=True,
            is_staff=True
        )
        user.set_password('12345')
        user.save()
