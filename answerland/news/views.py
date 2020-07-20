from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.urls import reverse_lazy
from answerland.news.models import News
from answerland.helpers import ajax_require, AuthorRequireMixin


class NewsListView(LoginRequiredMixin, ListView):
    model = News
    queryset = News.objects.filter(reply=False)
    paginate_by = 20
    # page_kwarg = "p"  # 默认page
    # context_object_name = "news_list"  # 默认模型类名_list或者object_list
    template_name = "news/news_list.html"
    # ordering = 'create_time'  # 多个排序("xx","xxx)

    # def get_ordering(self):
    #     pass
    #
    # def get_paginate_by(self, queryset):
    #     pass
    #
    # def get_queryset(self):
    #     pass
    #
    # def get_context_data(self, **kwargs):
    #     """添加额外上下文"""
    #     pass


class NewsDeleteView(LoginRequiredMixin, AuthorRequireMixin, DeleteView):
    model = News
    template_name = "news/news_confirm_delete.html"
    slug_url_kwarg = 'slug'  # 通过url删除对象组件id，默认值是slug
    pk_url_kwarg = 'pk'  # 通过url删除对象组件id，默认值是slug
    success_url = reverse_lazy("news:list")  # 在项目URLConf为加载前使用


@login_required
@ajax_require
@require_http_methods(["POST"])
def post_new(request):
    """发送动态，Ajax post请求"""
    post = request.POST["post"].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        # html = render_to_string("news/news_single.html", {"news": posted, "request": request})
        # return HttpResponse(html)
        return render(request, template_name="news/news_single.html", context={"news": posted})
    else:
        return HttpResponseBadRequest("内容不能为空")


@login_required
@ajax_require
@require_http_methods(["POST"])
def like_new(request):
    """点赞，Ajax post请求"""
    news_id = request.POST["news"].strip()
    news = News.objects.get(pk=news_id)
    news.switch_like(request.user)
    # 返回赞的数量
    return JsonResponse({"likes": news.like_count()})


@login_required
@ajax_require
@require_http_methods(["GET"])
def get_thread(request):
    """返回动态的评论"""
    news_id = request.GET["news"].strip()
    news = News.objects.get(pk=news_id)
    news_html = render_to_string("news/news_single.html", {"news": news})
    thread_html = render_to_string("news/news_thread.html", {"thread": news.get_thread()})

    return JsonResponse(
        {
            "uuid": news_id,
            "news": news_html,
            "thread": thread_html
        }
    )


@login_required
@ajax_require
@require_http_methods(["POST"])
def post_comment(request):
    """评论"""
    post = request.POST["reply"].strip()
    parent_id = request.POST["parent"]
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({"comments": parent.comment_count()})
    else:
        return HttpResponseBadRequest("内容不能为空")
