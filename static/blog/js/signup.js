// 注册
$(".btn").click(function () {
    $.ajax({
        url:"/signup/",
        type:"post",
        data:{
            csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
            nickname:$("#id_nickname").val(),
            username:$("#id_username").val(),
            password:$("#id_password").val(),
            confirm_password:$("#id_confirm_password").val(),
            email:$("#id_email").val(),
        },
        success:function (rep) {
            if (rep.code == 1000) {
                swal({
                    title: "注册成功",
                    text: "请牢记您的密码，因为站长还未开发找回密码功能。",
                    type: "success",
                    closeOnConfirm: true,
                    confirmButtonText: "确认",
                    confirmButtonClass: "btn-success"
                },
                function () {
                    $.ajax({
                        url:"/tosignin/",
                        type:"post",
                        data:{
                            csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
                            username:$("#id_username").val(),
                        },
                        success:function (rep) {
                            if (rep.code == 1000) {
                                location.href = "/"
                            }
                        }
                    })
                });
            }else {
                // 在提示错误信息之前，先清空原来的内容
                $("form span").html("");
                $("form .from-group").removeClass("has-error");
                // 开始循环获取对应字段
                $.each(rep.error, function (field, error_list) {
                    if (field == "__all__") {
                        var conPwd = $("#id_confirm_password");
                        conPwd.next().html(error_list[0]).css("color", "red");
                        conPwd.parent().addClass("has-error");
                    }else {
                        var idField = $("#id_"+field);
                        idField.next().html(error_list[0]).css("color", "red");
                        idField.parent().addClass("has-error");
                    }
                })
            }
        }
    })
});

$("#id_nickname").change(function () {
   $(this).parent().removeClass("has-error");
    $(this).next().html("");
});

$("#id_username").change(function () {
    $(this).parent().removeClass("has-error");
    $(this).next().html("");
});

$("#id_confirm_password").change(function () {
    $(this).parent().removeClass("has-error");
    $(this).next().html("");
});

$("#id_email").change(function () {
    $(this).parent().removeClass("has-error");
    $(this).next().html("");
});
