from django.http import HttpResponseRedirect


class UserloginMiddleware:
    """用户登录校验的中间件"""

    def process_request(self, request):
        """登陆验证"""
        urls = [
            '/user/',
            '/user/login_out/',
            '/user/address/',
            '/user/add_address/',
            '/user/edit_address/',
            '/user/del_address/',
            '/user/get_address_city/',
            '/user/get_address_district/',
            '/user/set_default_address/',
            '/cart/',
            '/cart/add_goods/',
        ]
        if request.path in urls:
            if not request.session.has_key('uid'):
                request.session['pre_url'] = request.path
                return HttpResponseRedirect('/user/login/')

