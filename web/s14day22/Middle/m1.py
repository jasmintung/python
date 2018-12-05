from django.utils.deprecation import MiddlewareMixin


class Row1(MiddlewareMixin):

    def process_request(self, request):
        print('row1_p_request')

    def process_views(self, request, view_func, view_func_args, view_func_kwargs):
        print('row1_p_views')

    def process_response(self, request, response):
        print('row1_p_response')
        return response


class Row2(MiddlewareMixin):

    def process_request(self, request):
        print('row2_p_request')

    def process_views(self, request, view_func, view_func_args, view_func_kwargs):
        print('row2_p_views')

    def process_response(self, request, response):
        print('row2_p_response')
        return response


from django.shortcuts import HttpResponse


class Row3(MiddlewareMixin):

    def process_views(self, request, view_func, view_func_args, view_func_kwargs):
        print('row3_p_view')

    def process_request(self,request):
        print('row3_p_request')

    def process_response(self, request, response):
        print('row3_p_response')
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ValueError):
            print("row3_p_exception")
            return HttpResponse('出现异常》。。')  # process_response依然会执行

    def process_template_response(self,request,response):
        # 如果Views中的函数返回的对象中，具有render方法
        print('gouzi define here')
        return response
