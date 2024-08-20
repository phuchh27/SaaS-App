from django.core.management.base import BaseCommand
from typing import Any
from subscriptions.models import Subscription


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        # print('hello world')
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            sub_perm = obj.permissions.all()
            # print('G: ', obj.groups.all())
            for group in obj.groups.all():
                group.permissions.set(sub_perm)
                # for per in obj.permissions.all():
                # group.permissions.add(per)
            # print('P: ', obj.permissions.all())
