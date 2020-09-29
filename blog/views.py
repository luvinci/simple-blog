import os
import json
import uuid
from bs4 import BeautifulSoup
from django.db.models import F
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blog import models
from utils.page import Pagination


def index(request):
    """
    博客首页
    :param request:
    :return:
    """
    current_page = request.GET.get("page")
    total_count = models.Article.objects.all().count()
    if total_count < 10:
        # 如果总数据小于每页显示数据10，则不分页
        articles = models.Article.objects.all().order_by("-id")
        data = {"articles": articles}
        return render(request, "index.html", data)
    else:
        page = Pagination(current_page, total_count, url_prefix="", per_page_num=10, max_page=7)
        articles = models.Article.objects.all().order_by("-id")[page.start_data:page.end_data]
        page_html = page.page_html()
        data = {"articles": articles, "page_html": page_html}
        return render(request, "index.html", data)


def user_home(request, username, **kwargs):
    """
    个人站点页面
    :param request:
    :param username: 当前站点的用户名
    :return:
    """
    try:
        current_page = request.GET.get("page")
        user = models.UserInfo.objects.filter(username=username).first()
        if not user:
            return redirect("/")
        nickname = user.nickname
        blog = user.blog
        if not kwargs:
            total_count = models.Article.objects.filter(blog=blog).count()
            if total_count < 10:
                articles = models.Article.objects.filter(blog=blog).order_by("-id")
                data = {"nickname": nickname, "username": username, "articles": articles}
                return render(request, "user_home.html", data)
            else:
                page = Pagination(current_page, total_count, url_prefix="", per_page_num=10, max_page=7)
                articles = models.Article.objects.filter(blog=blog).order_by("-id")[page.start_data:page.end_data]
                page_html = page.page_html()
                data = {"nickname": nickname, "username": username, "articles": articles, "page_html": page_html}
                return render(request, "user_home.html", data)
        else:
            condition = kwargs.get("condition")
            param = kwargs.get("param")
            if condition == "categoryid":
                param = param.replace("/", "")
                param = int(param.strip())
                articles = models.Article.objects.filter(blog=blog).filter(category__id=param).order_by("-id")
            elif condition == "tagid":
                param = param.replace("/", "")
                param = int(param.strip())
                articles = models.Article.objects.filter(blog=blog).filter(tags__id=param).order_by("-id")
            else:
                year, month = param.split("-")
                articles = models.Article.objects.filter(blog=blog).filter(publish_time__year=year, publish_time__month=month).order_by("-id")
            data = {"nickname": nickname, "username": username, "articles": articles}
            return render(request, "user_home.html", data)
    except Exception as e:
        return redirect("/")


def article_detail(request, username, article_id):
    """
    文章详情页
    :param request:
    :return:
    """
    try:
        user = models.UserInfo.objects.filter(username=username).first()
        if not user:
            return redirect("/")
        nickname = user.nickname
        article = models.Article.objects.filter(pk=article_id).first()
        if not article:
            return redirect("/")
        # 上一篇文章
        prev_article = models.Article.objects.filter(blog__user__username=username).filter(id__lt=article_id).order_by("-id").first()
        if not prev_article:
            prev_article = None
        # 下一遍文章
        next_article = models.Article.objects.filter(blog__user__username=username).filter(id__gt=article_id).order_by("id").first()
        if not next_article:
            next_article = None
        # 该文章的评论
        comments = models.Comment.objects.filter(article_id = article_id)
    except Exception as e:
        return redirect("/")
    data = {
        "nickname": nickname,
        "username": username,
        "article": article,
        "prev_article": prev_article,
        "next_article": next_article,
        "comments": comments
    }
    return render(request, "article_detail.html", data)


def article_up_down(request):
    """
    处理文章的推荐或反对
    :param request:
    :return:
    """
    rep = {"code": 1000}
    is_up = json.loads(request.POST.get("is_up"))
    article_id = int(request.POST.get("article_id"))
    user_id = request.user.pk
    obj = models.Article.objects.filter(pk=article_id).first()
    if obj.blog.user.username == request.user.username:
        rep["code"] = 1001
    else:
        try:
            with transaction.atomic():
                # 同一个用户操作第二次到这里一定会出异常
                obj = models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
                if obj:
                    if is_up:
                        models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
                    else:
                        models.Article.objects.filter(pk=article_id).update(down_count=F("down_count")+1)
        except Exception as e:
            # 捕获异常
            rep["code"] = 1002
            obj = models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first()
            if obj.is_up:
                rep["error"] = "你已经推荐过"
            else:
                rep["error"] = "你已经反对过"
    return JsonResponse(rep)


def article_comment(request):
    """
    文章评论
    :param request:
    :return:
    """
    rep = {"code": 1000}
    user_id = request.user.pk
    article_id = request.POST.get("article_id")
    parent_comment_id = request.POST.get("parent_comment_id")
    content = request.POST.get("content")
    bs = BeautifulSoup(content, "html.parser")
    for tag in bs.find_all():
        if tag.name == "script":
            tag.decompose()
    con = bs.text
    if not len(con):
        rep["code"] = 1002
        rep["error"] = "评论内容不能为空"
    else:
        try:
            with transaction.atomic():
                if not parent_comment_id:
                    obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, content=con)
                else:
                    obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, content=con, parent_comment_id=parent_comment_id)
                models.Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)
                rep["pub_time"] = obj.comment_time.strftime("%Y-%m-%d %H:%M")
                rep["article_content"] = obj.content
        except Exception as e:
            rep["code"] = 1001
            rep["error"] = "连接数据库出错"
    return JsonResponse(rep)


@login_required
def backend_article(request, **kwargs):
    """
    文章管理
    :param request:
    :param kwargs:
    :return:
    """
    current_page = request.GET.get("page")
    user = request.user
    blog = user.blog
    if not kwargs:
        total_count = models.Article.objects.filter(blog=blog).count()
        if total_count < 10:
            articles = models.Article.objects.filter(blog=blog).order_by("-id")
            return render(request, "backend_article.html", {"articles": articles})
        else:
            page = Pagination(current_page, total_count, url_prefix="", per_page_num=10, max_page=7)
            articles = models.Article.objects.filter(blog=blog).order_by("-id")[page.start_data: page.end_data]
            page_html = page.page_html()
            return render(request, "backend_article.html", {"articles": articles, "page_html": page_html})
    else:
        id = kwargs.get("id")
        id = int(id)
        if id == 0:
            total_count = models.Article.objects.filter(blog=blog).filter(category__id__isnull=True).count()
            if total_count < 10:
                articles = models.Article.objects.filter(blog=blog).filter(category__id__isnull=True).order_by("-id")
                return render(request, "backend_article.html", {"articles": articles})
            else:
                page = Pagination(current_page, total_count, url_prefix="", per_page_num=10, max_page=7)
                articles = models.Article.objects.filter(blog=blog).filter(category__id__isnull=True).order_by("-id")[page.start_data: page.end_data]
                page_html = page.page_html()
                return render(request, "backend_article.html", {"articles": articles, "page_html": page_html})
        else:
            total_count = models.Article.objects.filter(blog=blog).filter(category__id=id).count()
            if total_count < 10:
                articles = models.Article.objects.filter(blog=blog).filter(category__id=id).order_by("-id")
                return render(request, "backend_article.html", {"articles": articles})
            else:
                page = Pagination(current_page, total_count, url_prefix="", per_page_num=10, max_page=7)
                articles = models.Article.objects.filter(blog=blog).filter(category__id=id).order_by("-id")[page.start_data: page.end_data]
                page_html = page.page_html()
                return render(request, "backend_article.html", {"articles": articles, "page_html": page_html})


@login_required
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    blog = request.user.blog
    if request.method == "GET":
        categories = models.Category.objects.filter(blog=blog).values("id", "name")
        tags = models.Tag.objects.filter(blog=blog).values("id", "name")
        data = {"categories": categories, "tags": tags}
        return render(request, "article_add.html", data)
    else:
        rep = {"code": 1000}
        try:
            id = request.POST.get("id")
            title = request.POST.get("title")
            content = request.POST.get("content")
            category_id = request.POST.get("category")
            if category_id:
                category_id = int(category_id)
            tags = request.POST.getlist("tags")
            if not title.strip():
                rep["code"] = 1001
                rep["error"] = "文章标题不能为空"
            else:
                # 对标题进行过滤
                bs_title = BeautifulSoup(title, "html.parser")
                for tag in bs_title.find_all():
                    if tag.name == "script":
                        tag.decompose()
                # 对内容进行过滤
                bs_content = BeautifulSoup(content, "html.parser")
                for tag in bs_content.find_all():
                    if tag.name == "script":
                        tag.decompose()
                desc = str(bs_content.text[0:110]).strip() + "..."
                with transaction.atomic():
                    if not id:
                        obj = models.Article.objects.create(title=title, desc=desc, blog=blog, category_id=category_id)
                        models.ArticleDetail.objects.create(content=str(bs_content), article=obj)
                        if tags:
                            for tag_id in json.loads(tags[0]):
                                models.Article2Tag.objects.create(article=obj, tag_id=int(tag_id))
                    else:
                        obj = models.Article.objects.filter(id=int(id)).first()
                        models.ArticleDetail.objects.filter(article=obj).update(content=str(bs_content))
                        obj.title = title
                        obj.desc = desc
                        obj.blog = blog
                        obj.category_id = category_id
                        obj.save()
                        if tags:
                            models.Article2Tag.objects.filter(article_id=obj.id).delete()
                            for tag_id in json.loads(tags[0]):
                                models.Article2Tag.objects.create(article=obj, tag_id=int(tag_id))
        except Exception as e:
            rep["code"] = 1002
            rep["error"] = "发生未知错误，请稍后再试"
        return JsonResponse(rep)


def upload_image(request):
    """
    编辑文章上传图片
    :param request:
    :return:
    """
    obj = request.FILES.get("image")
    name, type = obj.name.split(".")
    random_str = str(uuid.uuid4())
    image = "{}.{}".format(random_str, type)
    path = os.path.join(settings.MEDIA_ROOT, "article_images", image)
    with open(path, "wb") as f:
        for chunk in obj.chunks():
            f.write(chunk)
    rep = {
        # 第一个参数表示没有错误，返回0
        "error": 0,
        "url": "/media/article_images/" + image,
    }
    return JsonResponse(rep)


@login_required
def delete_article(request):
    """
    删除文章
    :param request:
    :return:
    """
    rep = {"code": 1000}
    article_id = request.POST.get("article_id")
    try:
        obj = models.ArticleDetail.objects.filter(article_id=int(article_id)).first()
        html = obj.content
        bs = BeautifulSoup(html, "html.parser")
        for tag in bs.find_all():
            if tag.name == "img":
                path, img = tag["src"].rsplit("/", 1)
                img_path = os.path.join(settings.MEDIA_ROOT, "article_images", img)
                if os.path.exists(img_path):
                    os.remove(img_path)
        models.Article.objects.filter(id=int(article_id)).delete()
    except Exception as e:
        rep["code"] = 1002
    return JsonResponse(rep)


def edit_article(request, id):
    """
    编辑文章
    :param request:
    :param id:
    :return:
    """
    blog = request.user.blog
    article = models.Article.objects.filter(id=id).first()
    content = article.articledetail.content
    tag_list = []
    for tag in article.tags.all():
        tag_list.append(tag.pk)
    categories = models.Category.objects.filter(blog=blog).values("id", "name")
    tags = models.Tag.objects.filter(blog=blog).values("id", "name")
    data = {
        "article": article,
        "content": content,
        "tag_list": tag_list,
        "categories": categories,
        "tags": tags
    }
    return render(request, "article_edit.html", data)


@login_required
def backend_category(request):
    """
    分类界面
    :param request:
    :return:
    """
    user = request.user
    blog = user.blog
    categories = models.Category.objects.filter(blog=blog)
    return render(request, "backend_category.html", {"categories": categories})


@login_required
def delete_category(request):
    """
    删除分类
    :param request:
    :return:
    """
    rep = {"code": 1000}
    category_id = request.POST.get("category_id")
    try:
        obj = models.Category.objects.filter(id=int(category_id)).first()
        obj.article_set.clear()
        obj.delete()
    except Exception as e:
        rep["code"] = 1001
    return JsonResponse(rep)


@login_required
def add_category(request):
    """
    新增分类
    :param reqeust:
    :return:
    """
    rep = {"code": 1000}
    category_name = request.POST.get("category_name")
    if not category_name.strip():
        rep["code"] = 1003
        rep["error"] = "分类名不能为空"
    else:
        blog = request.user.blog
        try:
            obj = models.Category.objects.filter(name=category_name).first()
            if not obj:
                models.Category.objects.create(name=category_name, blog=blog)
            else:
                rep["code"] = 1001
                rep["error"] = "该分类已存在"
        except Exception as e:
            rep["code"] = 1002
    return JsonResponse(rep)


@login_required
def edit_category(request):
    """
    编辑分类
    :param request:
    :return:
    """
    rep = {"code": 1000}
    category_name = request.POST.get("category_name")
    category_id = request.POST.get("category_id")
    if not category_name.strip():
        rep["code"] = 1001
        rep["error"] = "不能修改为空的分类名"
    else:
        obj = models.Category.objects.filter(id=category_id).first()
        obj.name = category_name
        obj.save()
    return JsonResponse(rep)


@login_required
def backend_tag(request):
    """
    标签界面
    :param request:
    :return:
    """
    user = request.user
    blog = user.blog
    tags = models.Tag.objects.filter(blog=blog)
    return render(request, "backend_tag.html", {"tags": tags})


def delete_tag(request):
    """
    删除标签
    :param request:
    :return:
    """
    rep = {"code": 1000}
    tag_id = request.POST.get("tag_id")
    try:
        models.Article2Tag.objects.filter(tag_id=tag_id).delete()
        models.Tag.objects.filter(id=int(tag_id)).delete()
    except Exception as e:
        rep["code"] = 1001
    return JsonResponse(rep)


def add_tag(request):
    """
    新增标签
    :param request:
    :return:
    """
    rep = {"code": 1000}
    tag_name = request.POST.get("tag_name")
    if not tag_name.strip():
        rep["code"] = 1003
        rep["error"] = "标签名不能为空"
    else:
        blog = request.user.blog
        try:
            obj = models.Tag.objects.filter(name=tag_name).first()
            if not obj:
                models.Tag.objects.create(name=tag_name, blog=blog)
            else:
                rep["code"] = 1001
                rep["error"] = "该标签已存在"
        except Exception as e:
            rep["code"] = 1002
    return JsonResponse(rep)


def edit_tag(request):
    """
    编辑标签
    :param request:
    :return:
    """
    rep = {"code": 1000}
    tag_name = request.POST.get("tag_name")
    tag_id = request.POST.get("tag_id")
    if not tag_name.strip():
        rep["code"] = 1001
        rep["error"] = "不能修改为空的标签名"
    else:
        obj = models.Tag.objects.filter(id=tag_id).first()
        obj.name = tag_name
        obj.save()
    return JsonResponse(rep)


def setting(request):
    """
    修改密码
    :param request:
    :return:
    """
    return render(request, "setting.html")
