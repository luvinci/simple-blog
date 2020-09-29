// 删除文章
function delArticle(thz) {
    swal({
        title: "是否删除此文章",
        text: "",
        type: "warning",
        showCancelButton: true,
        cancelButtonClass: "btn-info",
        cancelButtonText: "取消",
        confirmButtonClass: "btn-danger",
        confirmButtonText: "确认",
        closeOnConfirm: true,
    },
    function () {
        var articleID = $(thz).attr("articleID");
        $.ajax({
            url: "/blog/article/delete/",
            type: "post",
            data: {
                "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
                article_id: articleID
            },
            success:function (rep) {
                if (rep.code == 1000) {
                    $(thz).parent().parent().remove();
                }else {
                    swal("删除失败，请稍后再试")
                }
            }
        })
    });
}