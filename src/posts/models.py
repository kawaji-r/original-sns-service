import uuid
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit.processors import ResizeToFit


class ObjectsManager(models.QuerySet):
    def all(self):
        return super().all().filter()

    def filter(self, *args, **kwargs):
        where = models.Q(user__is_active=True)
        where &= models.Q(*args, **kwargs)
        return super().filter(where)


class Post(models.Model):
    objects = ObjectsManager.as_manager()
    CHOICES_POST_CATEGORY = [
        (0, '投稿'),
        (1, 'リプライ'),
        (2, 'リポスト'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        'accounts.CustomUser', 
        verbose_name='ユーザ', 
        on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name='タイトル',
        max_length=20,
        null=True,
        blank=True)
    text = models.TextField(verbose_name='本文')
    photo = models.ImageField(
        verbose_name='投稿画像', 
        null=True,
        blank=True,
        upload_to='images/')
    post_image = ImageSpecField(
        source='photo',
        processors=[ResizeToFit(1080, 1080)],
        format='JPEG',
        options={'quality': 60})
    related_post = models.ForeignKey(
        'self',
        verbose_name='関連投稿',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    post_category = models.IntegerField(
        verbose_name='分類',
        choices=CHOICES_POST_CATEGORY,
        default=0)
    created_at = models.DateTimeField( 
        auto_now_add=True,
        blank=True)
    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True)
    
    def get_reply(self):
        replies = Post.objects.filter(related_post=self, post_category=1)
        return [reply for reply in replies]

    def get_like(self):
        likes = Like.objects.filter(post=self)
        return [like.user for like in likes]

    def get_repost(self):
        reposts = Post.objects.filter(related_post=self, post_category=2)
        return [repost.user for repost in reposts]

    def get_bookmark(self):
        bookmarks = Bookmark.objects.filter(post=self)
        return [bookmark.user for bookmark in bookmarks]


class Like(models.Model):
    objects = ObjectsManager.as_manager()
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        'accounts.CustomUser', 
        verbose_name='ユーザ', 
        on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post',
        verbose_name='投稿', 
        on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Bookmark(models.Model):
    objects = ObjectsManager.as_manager()
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        'accounts.CustomUser', 
        verbose_name='ユーザ', 
        on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post', 
        verbose_name='投稿', 
        on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')
