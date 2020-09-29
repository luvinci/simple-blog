// Ajax登录
$("#sign-in").click(function () {
    // 清除提示信息（账号或密码错误、验证码错误）
    $("#error_msg").remove();
    // 对账号和密码进行非空校验
    var username = $("#username").val();
    var password = $("#password").val();
    if (username.trim() == "") {
        $(".username").addClass("has-error");
        $(".username .pull-right").removeClass("hidden");
    }else {
        $(".username").removeClass("has-error");
        $(".username .pull-right").addClass("hidden");
    }
    if (password.trim() == "") {
        $(".password").addClass("has-error");
        $(".password .pull-right").removeClass("hidden");
    }else {
        $(".password").removeClass("has-error");
        $(".password .pull-right").addClass("hidden");
    }
    // 非空检验通过才发送Ajax
    if (username.trim() != "" || password.trim() != "") {
        $.ajax({
            url: "/signin/",
            type: "post",
            data: {
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
                username:username,
                password:password,
                valid_code:$("#valid_code").val(),
            },
            success: function (rep) {
                console.log(rep);
                if (rep.code == 1000){
                    location.href = "/"
                }else {
                    $("#error_msg").remove();
                    var divEle = document.createElement("div");
                    divEle.innerText = rep.error;
                    $(divEle).css("color", "red");
                    $(divEle).attr({"class": "form-group", "id": "error_msg"});
                    $(".form-horizontal").prepend(divEle);
                    $("#valid_img")[0].src += "?"
                }
            },
        });
    }
});

// 手动刷新验证码
$("#valid_img").click(function () {
    $(this)[0].src += "?";
});
