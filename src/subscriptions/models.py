from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
# Create your models here.

User = settings.AUTH_USER_MODEL

ALLOW_CUSTOM_GROUPS = True
SUBSCRIPTION_PERMISSIONS = [
    ('advanced', 'Advanced Perm'),
    ('pro', 'Pro Perm'),
    ('basic', 'Basic Perm'),
    ('basic_ai', 'Basic AI Perm'),
]


class Subscription(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission, limit_choices_to={
        "content_type__app_label": "subscriptions",
        "codename__in": [x[0]for x in SUBSCRIPTION_PERMISSIONS]
    }
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)


def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        sub_qs = Subscription.objects.filter(
            active=True)
        if subscription_obj is not None:
            sub_qs = sub_qs.exclude(id=subscription_obj.id)
        subs_gr = sub_qs.values_list('groups__id', flat=True)
        subs_gr_set = set(subs_gr)
        # groups_ids = groups.values_list('id', flat=True)
        current_groups = user.groups.all().values_list('id', flat=True)
        groups_ids_set = set(groups_ids)
        current_groups_set = set(current_groups) - subs_gr_set
        final_groups_id = list(groups_ids_set | current_groups_set)
        user.groups.set(final_groups_id)


post_save.connect(user_sub_post_save, sender=UserSubscription)
