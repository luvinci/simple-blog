// 删除分类
function delCategory(thz) {
    swal({
        title: "是否删除此分类",
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
        var categoryId = $(thz).attr("categoryId");
        $.ajax({
            url: "/blog/category/delete/",
            type: "post",
            data: {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                category_id: categoryId
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
// 新增分类
$("#add-btn").click(function () {
    var categoryName = $("#category").val();
    $.ajax({
        url: "/blog/category/add/",
        type: "post",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            category_name: categoryName
        },
        success: function (rep) {
            if (rep.code == 1000) {
                location.href = "/blog/backend/category/"
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
// 编辑分类
function editCategory(thz) {
    var categoryId = $(thz).attr("categoryId");
    var categoryName = $(thz).parent().parent().children().first()[0].innerText;
    $("#edit-cate-box").remove();
    $(".table").after("<div id='edit-cate-box'><input type='text'>" +
        "<button type='button' style='margin-left: 5px' onclick='editUpdate()'>修改</button>" +
        "<button type='button' style='margin-left: 5px' onclick='editCancel()'>取消</button></div>");
    $("#edit-cate-box>input").attr({"value": categoryName, "categoryid": categoryId});
}
// 编辑分类提交
function editUpdate() {
    var ele = $("#edit-cate-box>input");
    var categoryName = ele.val();
    var categoryId = ele.attr("categoryid");
    $.ajax({
        url: "/blog/category/edit/",
        type: "post",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            category_name: categoryName,
            category_id: categoryId
        },
        success: function (rep) {
            if (rep.code == 1000){
                location.href = "/blog/backend/category/"
            }else {
                swal(rep.error)
            }
        }
    })
}
// 编辑分类取消
function editCancel() {
    $("#edit-cate-box").remove();
}

