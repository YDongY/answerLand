# __Time__ : 2020/7/20 下午11:34
# __Author__ : '__YDongY__'

from django.http import HttpResponseBadRequest, HttpResponse
from functools import wraps
from django.views.generic import View
from django.core.exceptions import PermissionDenied


def ajax_require(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest("不是ajax请求")
        return f(request, *args, **kwargs)

    return wrap


class AuthorRequireMixin(View):
    """
    验证是否为原作者
    """

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
