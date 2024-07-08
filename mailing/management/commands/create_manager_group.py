from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает группу менеджеров и назначает необходимые права'

    def handle(self, *args, **options):
        # Создаем группу
        manager_group, created = Group.objects.get_or_create(name='manager')

        # Получаем права
        permissions = [
            Permission.objects.get(codename='view_all_mailings'),
            Permission.objects.get(codename='deactivate_mailing'),
            Permission.objects.get(codename='view_all_users'),
            Permission.objects.get(codename='deactivate_user'),
        ]

        # Назначаем права группе
        manager_group.permissions.set(permissions)
        manager_group.save()

        self.stdout.write(self.style.SUCCESS('Группа менеджеров создана и права назначены'))
