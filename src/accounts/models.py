import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nickname = models.CharField(
        _('nickname'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    id_regex = RegexValidator(
        regex=r'^[0-9a-zA-Z_]{5,15}$',
        message=('半角英数字または_(アンダースコア)のみ使用可能です。'))
    username = models.CharField(
        verbose_name='アカウントID',
        validators=[MinLengthValidator(5), id_regex],
        max_length=15,
        unique=True,
        error_messages={
            'unique': _("すでに存在するIDです"),
        },
    )
    # ユーザ、メール、パスワードはDjago標準
    description = models.TextField(
        verbose_name='自己紹介',
        null=True,
        blank=True)
    photo = models.ImageField(
        verbose_name='写真', 
        null=True,
        blank=True,
        upload_to='images/')
    thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(256, 256)],
        format='JPEG',
        options={'quality': 60})
    email = None

    def get_follower(self):
        followers = Follow.objects.filter(follow_to=self)
        return [follower.follow_from for follower in followers]

    class Meta:
        verbose_name_plural = 'CustomUser'


class ObjectsManager(models.QuerySet):
    def all(self):
        return super().all().filter()

    def filter(self, *args, **kwargs):
        where = models.Q(follow_from__is_active=True)
        where &= models.Q(follow_to__is_active=True)
        where &= models.Q(*args, **kwargs)
        return super().filter(where)


class Follow(models.Model):
    objects = ObjectsManager.as_manager()
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    follow_from = models.ForeignKey(
        'accounts.CustomUser', 
        verbose_name='フォロワー', 
        related_name='follow_from',
        on_delete=models.CASCADE)
    follow_to = models.ForeignKey(
        'accounts.CustomUser', 
        verbose_name='フォロー', 
        related_name='follow_to',
        on_delete=models.CASCADE)
    created_at = models.DateTimeField( 
        auto_now_add=True,
        blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follow_from", "follow_to"],
                name="follow_unique"
            ),
        ]
