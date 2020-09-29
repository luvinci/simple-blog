class Pagination(object):
    """
    一个用于分页的类
    """
    def __init__(self, current_page, total_count, url_prefix, per_page_num=10, max_page=11):
        """
        :param current_page: 当前页码数
        :param total_count: 总的数据
        :param url_prefix: a标签href的前缀
        :param per_page_num: 默认每页显示10条数据
        :param max_page: 默认每个页面最多显示11个页码
        """
        self.url_prefix = url_prefix
        self.max_page = max_page

        # 总页数，余页 = 总数据/每页显示数据
        total_page, remainder = divmod(total_count, per_page_num)
        if not total_page:
            total_page = 1
        if remainder:
            total_page += 1
        self.total_page = total_page

        try:
            current_page = int(current_page)
            # 如果输入的页码数超过了最大的页码数，默认返回最后一页
            if current_page > total_page:
                current_page = total_page
        except Exception:
            # 当输入的页码不是数字的时候，默认返回第一页
            current_page = 1
        self.current_page = current_page

        # 定义两个变量保存数据从哪儿取到哪儿
        self.data_start = (current_page - 1) * per_page_num
        self.data_end = current_page * per_page_num

        # 页面总共展示多少条页码
        if total_page < self.max_page:
            self.max_page = total_page
        half_max_page = self.max_page // 2

        # 页面上展示的页码从哪开始
        page_start = current_page - half_max_page
        # 页面上展示的页码到哪结束
        page_end = current_page + half_max_page
        if page_start <= 1:
            page_start = 1
            page_end = self.max_page
        if page_end >= total_page:
            page_end = total_page
            page_start = total_page - self.max_page + 1
        self.page_start = page_start
        self.page_end = page_end

    @property
    def start_data(self):
        return self.data_start

    @property
    def end_data(self):
        return self.data_end

    def page_html(self):
        # 自己拼接分页的html代码
        html_str_list = []
        # 首页
        html_str_list.append('<li><a href="{}?page=1">首页</a></li>'.format(self.url_prefix))
        # 判断 如果是第一页，就没有上一页
        if self.current_page <= 1:
            html_str_list.append('<li class="disabled"><a href="#"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.current_page - 1))
        else:
            html_str_list.append('<li><a href="{}?page={}"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.url_prefix, self.current_page - 1))
        # 中间显示的页数
        for i in range(self.page_start, self.page_end+1):
            # 如果是当前页就加一个active样式类
            if i == self.current_page:
                tmp = '<li class="active"><a href="{0}?page={1}">{1}</a></li>'.format(self.url_prefix, i)
            else:
                tmp = '<li><a href="{0}?page={1}">{1}</a></li>'.format(self.url_prefix, i)
            html_str_list.append(tmp)
        # 判断 如果是最后一页，就没有下一页
        if self.current_page >= self.total_page:
            html_str_list.append('<li class="disabled"><a href="#"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            html_str_list.append('<li><a href="{}?page={}"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.url_prefix, self.current_page + 1))
        # 尾页
        html_str_list.append('<li><a href="{}?page={}">尾页</a></li>'.format(self.url_prefix, self.total_page))
        page_html = "".join(html_str_list)
        return page_html
