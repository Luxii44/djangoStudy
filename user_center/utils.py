from django.shortcuts import redirect


def check_login(func_target):
    def fun(request, *args, **kwargs):
        # 檢測用戶是否登录
        if request.session.has_key('uid'):
            return func_target(request, *args, **kwargs)
        else:
            return redirect('/user/login')
    return fun