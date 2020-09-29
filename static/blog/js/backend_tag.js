// 删除标签
function delTag(thz) {
    swal({
        title: "是否删除此标签",
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
        var tagId = $(thz).attr("tagId");
        $.ajax({
            url: "/blog/tag/delete/",
            type: "post",
            data: {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                tag_id: tagId
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
// 新增标签
$("#add-btn").click(function () {
    var tagName = $("#tag").val();
    $.ajax({
        url: "/blog/tag/add/",
        type: "post",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            tag_name: tagName
        },
        success: function (rep) {
            if (rep.code == 1000) {
                location.href = "/blog/backend/tag/"
            }else if (rep.code == 1001){
                swal(rep.error)
            }else if (rep.code == 1003){
                swal(rep.error)
            }else {
                swal("添加失败")
            }
        }
    })
});
// 编辑标签
function editTag(thz) {
    var tagId = $(thz).attr("tagId");
    var tagName = $(thz).parent().parent().children().first()[0].innerText;
    $("#edit-tag-box").remove();
    $(".table").after("<div id='edit-tag-box'><input type='text'>" +
        "<button type='button' style='margin-left: 5px' onclick='editUpdate()'>修改</button>" +
        "<button type='button' style='margin-left: 5px' onclick='editCancel()'>取消</button></div>");
    $("#edit-tag-box>input").attr({"value": tagName, "tagid": tagId});
}
// 编辑标签提交
function editUpdate() {
    var ele = $("#edit-tag-box>input");
    var tagName = ele.val();
    var tagId = ele.attr("tagid");
    $.ajax({
        url: "/blog/tag/edit/",
        type: "post",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            tag_name: tagName,
            tag_id: tagId
        },
        success: function (rep) {
            if (rep.code == 1000){
                location.href = "/blog/backend/tag/"
            }else {
                swal(rep.error)
            }
        }
    })
}
// 编辑标签取消
function editCancel() {
    $("#edit-tag-box").remove();
}
