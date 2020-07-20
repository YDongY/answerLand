from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"
    slug_field = "username"
    # 对应url位置参数 path("<str:username>/", views.UserDetailView.as_view(), name="detail"),
    slug_url_kwarg = "username"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["nickName", "email", "avatar", "job_title", "introduction", "location", "personal_url",
              "weibo_url", "zhihu_url", "github_url", "LinkedIn_url"]

    template_name = "users/user_form.html"

    def get_success_url(self):
        """更新成功跳转页面"""
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user
