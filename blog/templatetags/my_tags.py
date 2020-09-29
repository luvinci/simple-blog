"""
自定义模板包含标签
"""
import datetime
from django import template
from django.db.models import Count
from django.shortcuts import render
from blog import models

register = template.Library()


@register.inclusion_tag("side_bar.html")
def get_side_bar(request, username):
    """
    侧边栏，获取"标签"、"文章分类"、"日期归档"归类名称及其对应数量
    :param request:
    :param username: 本站的博主
    :return:
    """
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, "index.html")
    blog = user.blog
    # 查询当前站点的每一个分类以及对应的文章数
    categories = models.Category.objects.filter(blog=blog).annotate(num=Count("article")).values_list("name", "num", "id")
    # 查询当前站点的每一个标签以及对应的文章数
    tags = models.Tag.objects.filter(blog=blog).annotate(num=Count("article")).values_list("name", "num", "id")
    # 查询当前站点的每一个归档以及对应的文章数
    """
    extra() 能在QuerySet生成的SQL从句中注入新子句，即QuerySet能调extra()方法。
    ...extra(select={"ym": "DATE_FORMAT(publish_time, '%%Y-%%m')"})执行完了，相当于在
    QuerySet缓存中多生成了一个"ym"字段，它对应的值可以说是一条"SQL语句 / SQL中的内容"；
    如：select={"time": "publish_time > '2011-11-11'"}；ORM中是没有 > 这种操作的。
    """
    archives = models.Article.objects.filter(blog__user__username=username).extra(
        select={"ym": "DATE_FORMAT(publish_time, '%%Y-%%m')"}).values("ym").annotate(
        num=Count("id")).values_list("ym", "num")
    data = {
        "username": username,
        "categories": categories,
        "tags": tags,
        "archives": archives
    }
    return data


@register.simple_tag
def usage_time(username):
    """
    计算用户园龄
    :param reg_time:
    :return:
    """
    user = models.UserInfo.objects.filter(username=username).first()
    reg_data = user.reg_data
    timedelta = datetime.date.today() - reg_data
    return timedelta.days


@register.inclusion_tag("backend_side_bar.html")
def backend_side_bar(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    categories = models.Category.objects.filter(blog=blog).annotate(num=Count("article")).values_list("name", "num", "id")
    data = {
        "categories": categories
    }
    return data
