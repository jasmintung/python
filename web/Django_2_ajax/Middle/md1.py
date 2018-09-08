from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.handlers.wsgi import WSGIRequest


class UrlFilter(MiddlewareMixin):

    def process_request(self, request):
        """
        一个简单的例子
        假如用户输入http://127.0.0.1:9998/12312/那么会直接给用户返回:”无权访问"
        :param request:
        :return:
        """
        print("UrlFilter:", request)
        print(request.path)
        if request.path.startswith("/usdb/"):
            pass
        else:
            return HttpResponseForbidden("无权访问!")

    def process_views(self, request, view_func, view_func_args, view_func_kwargs):
        print("process_views")

    def process_response(self, request, response):
        return response
