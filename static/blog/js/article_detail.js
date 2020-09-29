// 推荐或反对
$(".thumb").click(function () {
    var isLogin = $("#is-login").attr("user");
    // 如果这个值不是匿名用户，则用户已登录
    if (isLogin != "AnonymousUser") {
        // 用于后端判断是推荐还是反对
        var is_up = $(this).hasClass("thumbs-up");
        // 当前文章ID
        var article_id = $("#is-login").attr("article_id");
        $.ajax({
            url:"/blog/updown/",
            type:"post",
            data:{
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
                "is_up": is_up,
                "article_id": article_id
            },
            success:function (rep) {
                $(".upDown>.msg").text("");
                if (rep.code == 1000) {  // 推荐或反对成功
                    if (is_up) { // 推荐
                        var up = $(".thumbs-up>.num");
                        up.text(parseInt(up.text())+1);
                        var info_up = $("#zan");
                        info_up.text(parseInt(info_up.text())+1)
                    }else { // 反对
                        var down = $(".thumbs-down>.num");
                        down.text(parseInt(down.text())+1)
                    }
                }else { // 失败
                    if (rep.code == 1001) {
                        if(is_up) {
                            $(".upDown>.msg").text("你不能推荐自己的内容").css("color", "red");
                        }else {
                            $(".upDown>.msg").text("你不能反对自己的内容").css("color", "red");
                        }
                        setTimeout(function () {
                            $(".upDown>.msg").text("");
                        }, 1000)
                    }else {
                        $(".upDown>.msg").text(rep.error).css("color", "red");
                        setTimeout(function () {
                            $(".upDown>.msg").text("");
                        }, 1000)
                    }
                }
            }
        })
    }else {
        swal({
            title: "操作失败",
            text: "需要登录才能推荐或反对，是否登录？",
            type: "warning",
            showCancelButton: true,
            cancelButtonText: "取消",
            confirmButtonClass: "btn-success",
            confirmButtonText: "好的",
            closeOnConfirm: true,
        },
        function () {
            location.href = "/signin/"
        })
    }
});


// 评论
var parent_comment_id = "";  // 定义父评论ID

$(".comment-input>.btn").click(function () {  // 提交评论
     var isLogin = $("#is-login").attr("user");
     // 如果这个值不是匿名用户，则用户已登录
    if (isLogin !== "AnonymousUser") {
        if ($("#id_editor").val().charAt(0) !== "@") {  // 说明没有父评论
            parent_comment_id = "";
        }
        var content = $("#id_editor").val();
        $.ajax({
            url: "/blog/comment/",
            type: "post",
            data: {
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
                article_id:$("#is-login").attr("article_id"),
                parent_comment_id: parent_comment_id,
                content:content,
            },
            success:function (rep) {
                if (rep.code == 1000) {
                    var username = $("#is-login").attr("username");
                    var avatar = $("#is-login").attr("avatar");
                    var pk = $("#is-login").attr("pk");
                    var time = rep.pub_time;
                    var article_content = rep.article_content;
                    var html = '<div class="comment-item clearfix">' + '<div class="avatar"><a href=/blog/' + username +
                        '"><img src=/"' + avatar + '"></a></div><div class="con"><div class="clearfix"><div class="user"><span>' +
                        time + '</span><a href="/blog/' + username + '">' + username + '</a></div><div class="reply"><a href="javascript:void(0);" username="' +
                        username + '" pk="' + pk + '"><i class="fa fa-comment-o">&nbsp;回复</i></a> </div></div><div class="reply-con">' + article_content + '</div></div></div>';
                    $(".comment-content").append(html);
                }else {
                    swal(rep.error)
                }
                $("#id_editor").val("");
                parent_comment_id="";
            }
        })
    }else {
        swal({
            title: "操作失败",
            text: "需要登录才能评论，是否登录？",
            type: "warning",
            showCancelButton: true,
            cancelButtonText: "取消",
            confirmButtonClass: "btn-success",
            confirmButtonText: "好的",
            closeOnConfirm: true,
        },
        function () {
            location.href = "/signin/"
        })
    }
});

// 回复
$(".reply>a").click(function () {
    var isLogin = $("#is-login").attr("user");
    if (isLogin !== "AnonymousUser") {
        var val = "@" + $(this).attr("username") + "\n";
        $("#id_editor").val(val);
        parent_comment_id = $(this).attr("pk")
    }else {
        swal({
            title: "操作失败",
            text: "需要登录才能回复，是否登录？",
            type: "warning",
            showCancelButton: true,
            cancelButtonText: "取消",
            confirmButtonClass: "btn-success",
            confirmButtonText: "好的",
            closeOnConfirm: true,
        },
        function () {
            location.href = "/signin/"
        })
    }
});


