from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    用户登录认证
    """

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)