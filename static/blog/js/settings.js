// 修改密码
var newPassword = $("#id-password");
var confirmPassword = $("#id-confirm-password");

function checkPassword(thz) {
    if (newPassword.val().trim() == "") {
        $("#error").remove();
        $("#empty-error1").remove();
        var error = $("<span id='empty-error1'></span>");
        error.text("新密码不能为空");
        error.css("color", "red");
        thz.after(error[0])
    }else if(confirmPassword.val().trim() !== ""){
        $("#empty-error1").remove();
        $("#error").remove();
        if (newPassword.val().trim() !== confirmPassword.val().trim()) {
            var errorEle = $("<div id='error'></div>");
            errorEle.text("两次密码不一致");
            errorEle.css("color", "red");
            $("#password-box .panel-body").prepend(errorEle)
        }
    }else {
        $("#empty-error1").remove();
    }
}

function checkConfirmPassword(thz) {
    if (confirmPassword.val().trim() == ""){
        $("#error").remove();
        $("#empty-error2").remove();
        var error = $("<span id='empty-error2'></span>");
        error.text("确认密码不能为空");
        error.css("color", "red");
        thz.after(error[0])
    }else {
        $("#empty-error2").remove();
        $("#error").remove();
        if (newPassword.val().trim() !== confirmPassword.val().trim()) {
            var errorEle = $("<div id='error'></div>");
            errorEle.text("两次密码不一致");
            errorEle.css("color", "red");
            $("#password-box .panel-body").prepend(errorEle)
        }
    }
}

$("#btn-password").click(function () {
    if (newPassword.val().trim() !== "" || confirmPassword.val().trim() !== "" || $("#empty-error1").length === 0 || $("#empty-error2").length === 0){
        $.ajax({
            url: "/password/",
            type: "post",
            data: {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                password: newPassword.val(),
                confirm_password: confirmPassword.val()
            },
            success: function (rep) {
                if (rep.code == 1000){
                    swal({
                        title: "修改密码成功",
                        text: "请牢记您的密码，因为站长还未开发找回密码功能。",
                        type: "success",
                        closeOnConfirm: true,
                        confirmButtonText: "确认",
                        confirmButtonClass: "btn-success"
                    },
                    function () {
                        location.href = "/signin/"
                    })
                }else {
                    $.each(rep.error, function (field, error_list) {
                        if (field == "password") {
                            swal(error_list[0])
                        }
                    })
                }
            }
        })
    }
});


// 修改昵称
var nickname = $("#id-nickname");
$("#btn-nickname").click(function () {
    if (nickname.val().trim() == "") {
        $("#nickname-error").remove();
        var errorEle = $("<div id='nickname-error'></div>");
        errorEle.text("请输入昵称");
        errorEle.css("color", "red");
        $("#nickname-box .panel-body").prepend(errorEle)
    }else {
        $.ajax({
            url: "/nickname/",
            type: "post",
            data: {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                nickname: nickname.val()
            },
            success: function (rep) {
                if (rep.code == 1000) {
                    swal({
                        title: "修改成功",
                        type: "success",
                        closeOnConfirm: true,
                        confirmButtonText: "确认",
                        confirmButtonClass: "btn-success"
                    },
                    function () {
                        location.href = "/blog/backend/"
                    })
                }else {
                    $.each(rep.error, function (field, error_list) {
                        if (field == "nickname") {
                            swal(error_list[0])
                        }
                    })
                }
            }
        })
    }
});

function checkNickname() {
    if ($("#id-nickname").val().trim() !== "") {
        $("#nickname-error").remove();
    }
}