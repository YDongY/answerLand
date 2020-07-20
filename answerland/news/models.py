from django.db import models
import uuid
# Create your models here.
from utils.base_model import BaseModel
from django.conf import settings
from answerland.users.models import User


class News(BaseModel):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name="publisher", verbose_name="用户")

    parent = models.ForeignKey("self", blank=True, null=True, related_name="thread", on_delete=models.CASCADE,
                               verbose_name="自关联")
    content = models.TextField(verbose_name="内容")
    liked = models.ManyToManyField(User, related_name="liked_news", verbose_name="点赞用户")
    reply = models.BooleanField(default=False, verbose_name="是否评论")

    class Meta:
        verbose_name = "首页"
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)

    def __str__(self):
        return self.content

    def switch_like(self, user):
        if user in self.liked.all():
            self.liked.remove(user)
        else:
            self.liked.add(user)

    def get_parent(self):
        if self.parent:
            return self.parent
        else:
            return self

    def reply_this(self, user, text):
        parent = self.get_parent()
        News.objects.create(
            user=user,
            reply=True,
            content=text,
            parent=parent
        )

    def get_thread(self):
        parent = self.get_parent()
        return parent.thread.all()

    def comment_count(self):
        return self.get_thread().count()

    def like_count(self):
        return self.liked.count()

    def get_likers(self):
        return self.liked.all()
