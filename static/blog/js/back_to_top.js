var backBtn=$("#back-to-top");
function backToTop() {
    $("html,body").animate({
        scrollTop: 0
    }, 800);
}
backBtn.on("click", backToTop);

// 当滚动条的垂直位置大于浏览器所能看到的页面的那部分的高度时，回到顶部按钮就显示
$(window).on("scroll", function () {
    if ($(window).scrollTop() > $(window).height())
        backBtn.fadeIn();
    else
        backBtn.fadeOut();
});

// 触发滚动事件，避免刷新的时候显示回到顶部按钮
$(window).trigger("scroll");
