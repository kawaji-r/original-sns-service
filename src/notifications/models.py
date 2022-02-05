import uuid
from django.db import models


class ObjectsManager(models.QuerySet):
    def all(self):
        return super().all().filter()

    def filter(self, *args, **kwargs):
        where = models.Q(user__is_active=True)
        where &= models.Q(*args, **kwargs)
        return super().filter(where)


class Notification(models.Model):
    objects = ObjectsManager.as_manager()
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    text = models.TextField(verbose_name='お知らせ')
    user = models.ForeignKey(
        'accounts.CustomUser',
        related_name='user',
        verbose_name='ユーザ', 
        on_delete=models.CASCADE
    )
    action_user = models.ForeignKey(
        'accounts.CustomUser',
        related_name='action_user',
        verbose_name='アクションを起こしたユーザ', 
        on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='削除ステータス'
    )
    created_at = models.DateTimeField(
        auto_now=True,
        blank=False
    )