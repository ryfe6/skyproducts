from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.contrib.auth.models import Permission
from users.models import User


class Command(BaseCommand):
    """Скрипт для создания группы модератора в админке."""
    def handle(self, *args, **options):
        moderator_group, created = Group.objects.get_or_create(name='moderator')
        moderator_group.permissions.add(Permission.objects.get(codename='cancel_product_publication'))
        moderator_group.permissions.add(Permission.objects.get(codename='change_product_description'))
        moderator_group.permissions.add(Permission.objects.get(codename='change_product_category'))
        moderator_group.permissions.add(Permission.objects.get(codename='add_product'))
        moderator_group.permissions.add(Permission.objects.get(codename='change_product'))
        moderator_group.permissions.add(Permission.objects.get(codename='delete_product'))

        # Введите _email пользователя, который будет наделен правами модератора
        _email = "denis.koptelev@gmail.com"
        if _email == "_":
            print("Группа moderator создана")
        else:
            user = User.objects.get(email=_email)
            user.groups.add(moderator_group)
            print("Группа moderator создана и пользователь успешно добавлен")
