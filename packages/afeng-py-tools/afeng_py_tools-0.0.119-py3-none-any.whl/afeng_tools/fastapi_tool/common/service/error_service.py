from abc import ABCMeta, abstractmethod

from starlette.requests import Request

from afeng_tools.application_tool.application_models import AppInfo
from afeng_tools.fastapi_tool.core.fastapi_items import ResponseTemplateResult
from afeng_tools.fastapi_tool.core.fastapi_response import template_resp, json_resp
from afeng_tools.http_tool import http_request_tools


class ErrorService(metaclass=ABCMeta):

    @abstractmethod
    def handle_404(self, message: str = '您访问的资源不存在！', request: Request = None, context_data: dict = None,
                   app_info: AppInfo = None):
        return json_resp(error_no=404, message=message)

    @abstractmethod
    def handle_500(self, message: str = '服务器内部错误！', request: Request = None, context_data: dict = None,
                   app_info: AppInfo = None):
        return json_resp(error_no=500, message=message)

    @abstractmethod
    def handle_501(self, message: str = '操作失败！', request: Request = None, context_data: dict = None,
                   app_info: AppInfo = None):
        return json_resp(error_no=501, message=message)


class DefaultErrorService(ErrorService):
    """默认错误处理"""

    def handle_response(self, request: Request, app_info: AppInfo, error_no: int, title: str, message: str,
                        template_file: str,
                        context_data: dict):
        if request and not http_request_tools.is_json(request.headers) and not (app_info and app_info.is_json_api):
            resp_result = ResponseTemplateResult(title=title, message=message,
                                                 template_file=f'common/{template_file}',
                                                 context_data=context_data)
            app_info = app_info if app_info else request.scope.get('app_info')
            if context_data and 'template_file' in context_data:
                resp_result.template_file = resp_result.context_data['template_file']
            elif app_info:
                resp_result.template_file = f'{app_info.code}/{template_file}'
            return template_resp(request=request, resp_result=resp_result, app_info=app_info)
        return json_resp(error_no=error_no, message=message)

    def handle_404(self, message: str = '您访问的资源不存在！', request: Request = None, context_data: dict = None,
                   app_info: AppInfo = None):
        return self.handle_response(request=request, app_info=app_info, error_no=404, title='404错误页面',
                                    message=message,
                                    template_file='views/error/404.html', context_data=context_data)

    def handle_500(self, message: str = '服务器内部错误！', request: Request = None, context_data: dict = None,
                   app_info: AppInfo = None):
        return self.handle_response(request=request, app_info=app_info, error_no=500, title='500错误页面',
                                    message=message,
                                    template_file='views/error/500.html', context_data=context_data)

    def handle_501(self, message: str = '操作失败！', request: Request = None, context_data: dict = None,
                   app_info: AppInfo = None):
        return self.handle_response(request=request, app_info=app_info, error_no=501, title='操作失败页面',
                                    message=message,
                                    template_file='views/error/501.html', context_data=context_data)
