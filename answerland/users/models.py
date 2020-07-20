from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from answerland.utils.base_model import BaseMixin


class User(AbstractUser, BaseMixin):
    """
    自定义模型
    """
    nickName = models.CharField(blank=True, null=True, max_length=255, verbose_name="昵称")
    job_title = models.CharField(max_length=50, null=True, blank=True, verbose_name="职称")
    introduction = models.TextField(null=True, blank=True, verbose_name="简介")
    avatar = models.ImageField(upload_to="profile_pics/", null=True, blank=True, verbose_name="头像")
    location = models.CharField(max_length=50, null=True, blank=True, verbose_name="位置")
    personal_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="个人连接")
    weibo_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="微博连接")
    zhihu_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="连接连接")
    github_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="github连接")
    LinkedIn_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="LinkedIn连接")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_profile_name(self):
        if self.nickName:
            return self.nickName
        else:
            return self.username

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
