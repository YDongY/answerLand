# __Time__ : 2020/7/20 上午11:59
# __Author__ : '__YDongY__'
from django.db import models


class BaseMixin(object):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

