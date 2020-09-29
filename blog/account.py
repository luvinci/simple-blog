import io
import random
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect

from blog.forms import AccountForm, SetPassword, SetNickname
from blog import models


def agreement(request):
    """
    用户协议
    :param request:
    :return:
    """
    return render(request, "agreement.html")


def get_random_color():
    """
    返回一个元祖，用于给验证码图片的干扰线和干扰点上颜色
    :return:
    """
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_valid_code(request):
    """
    随机生成验证码图片
    :param request:
    :return:
    """
    image = Image.new("RGB", (136, 34), "rgb(220, 220, 220)")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("static/blog/font/traditional.ttf", size=34)
    # 生成5个随机字母或数字
    valid_list = []
    for i in range(1, 6):
        number = str(random.randint(0, 9))
        lower_letter = chr(random.randint(97, 122))
        upper_letter = chr(random.randint(65, 90))
        random_char = random.choice([number, lower_letter, upper_letter])
        draw.text((i*22, 0), random_char, fill="black", font=font)
        valid_list.append(random_char)
    width = 136
    height = 36
    # 画干扰线
    for i in range(3):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    # 画干扰点
    for i in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point([x, y], fill=get_random_color())
    # 将验证码图片写入内存
    stream = io.BytesIO()
    image.save(stream, "png")
    valid_image = stream.getvalue()
    stream.close()
    # 将验证码图片对应的字符串保存到session
    valid_str = "".join(valid_list)
    request.session["valid_str"] = valid_str
    return HttpResponse(valid_image)


def sign_up(request):
    """
    基于Form组件和Ajax实现注册
    :param request:
    :return:
    """
    rep = {"code": 1000, "error": None}
    form = AccountForm()
    if request.method == "GET":
        return render(request, "signup.html", {"form": form})
    if request.is_ajax():
        form = AccountForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data.get("nickname")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            models.UserInfo.objects.create_user(nickname=nickname, username=username, password=password, email=email)
            obj = models.UserInfo.objects.filter(username=username).first()
            models.Blog.objects.create(user_id=obj.pk, name=username)
        else:
            rep["code"] = 1001
            rep["error"] = form.errors
        return JsonResponse(rep)


def to_sign_in(request):
    """
    用户注册成功后，取消设置安全问题时则执行此函数，用于保存用户状态，不需要用户再次登录
    :param request:
    :return:
    """
    rep = {"code": 1000, "error": None}
    username = request.POST.get("username")
    user = models.UserInfo.objects.filter(username=username).first()
    login(request, user)
    return JsonResponse(rep)


def sign_in(request):
    """
    基于Ajax实现登录
    :param request:
    :return:
    """
    rep = {"code": 1000, "error": None}
    if request.method == "GET":
        return render(request, "signin.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        valid_code = request.POST.get("valid_code")
        valid_str = request.session.get("valid_str", None)

        if valid_code.upper() == valid_str.upper():
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(rep)
            else:
                rep["code"] = 1001
                rep["error"] = "用户名或密码错误"
                return JsonResponse(rep)
        else:
            rep["code"] = 1002
            rep["error"] = "验证码错误"
            return JsonResponse(rep)


def log_out(request):
    """
    退出登录
    :param request:
    :return:
    """
    logout(request)
    return redirect("/")

def set_nickname(request):
    """
    修改昵称
    :param request:
    :return:
    """
    rep = {"code": 1000}
    username = request.user.username
    form = SetNickname(request.POST)
    if form.is_valid():
        nickname = form.cleaned_data.get("nickname")
        models.UserInfo.objects.filter(username=username).update(nickname=nickname)
    else:
        rep["code"] = 1001
        rep["error"] = form.errors
    return JsonResponse(rep)


def set_password(request):
    """
    修改密码
    :param request:
    :return:
    """
    rep = {"code": 1000}
    user = request.user
    form = SetPassword(request.POST)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
    else:
        rep["code"] = 1001
        rep["error"] = form.errors
    return JsonResponse(rep)
