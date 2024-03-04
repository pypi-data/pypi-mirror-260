import json
import os.path
from typing import Any, Optional, Mapping, Sequence

from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import FileResponse, Response, RedirectResponse

from afeng_tools.application_tool.application_models import AppInfo
from afeng_tools.fastapi_tool.common.service import fastapi_error_service
from afeng_tools.fastapi_tool.core.fastapi_response import json_resp
from afeng_tools.fastapi_tool.fastapi_jinja2_tools import create_template_response
from afeng_tools.sqlalchemy_tools.core.sqlalchemy_base_model import is_model_instance
from afeng_tools.sqlalchemy_tools.tool import sqlalchemy_model_tools


def resp_404(message: str | Sequence = '页面没找到！', request: Request = None, context_data: dict = None,
             app_info: AppInfo = None):
    return fastapi_error_service.handle_404(message=message, request=request, context_data=context_data,
                                            app_info=app_info)


def resp_501(message: str | Sequence, request: Request = None, context_data: dict = None, app_info: AppInfo = None):
    return fastapi_error_service.handle_501(message=message, request=request, context_data=context_data,
                                            app_info=app_info)


def resp_500(message: str | Sequence = '服务器内部错误！', request: Request = None, context_data: dict = None,
             app_info: AppInfo = None):
    return fastapi_error_service.handle_500(message=message, request=request, context_data=context_data,
                                            app_info=app_info)


def resp_template(request: Request, template_file: str, context_data: dict[str, Any]):
    """响应模板"""
    return create_template_response(request=request, template_file=template_file, context=context_data)


def resp_json(data: Any = None, error_no: int = 0, message: str | Sequence = 'success', app_info: AppInfo = None):
    if is_model_instance(data) or (data and isinstance(data, list) and len(data) > 0 and is_model_instance(data[0])):
        data = json.loads(sqlalchemy_model_tools.to_json(data))
    if isinstance(data, BaseModel):
        data = data.model_dump(mode='json')
    return json_resp(error_no=error_no, message=message, data=data)


def resp_file(file_path: str, file_name: str = None, download_flag: bool = False,
              context_data: dict = None, app_info: AppInfo = None) -> Response:
    """响应文件"""
    if not os.path.exists(file_path):
        return resp_404(message='您访问的资源不存在！', context_data=context_data, app_info=app_info)
    response = FileResponse(file_path)
    with open(file_path, "rb") as file:
        if download_flag:
            if file_name is None:
                file_name = os.path.split(file_path)[1]
            response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
        response.body = file.read()
        return response


def redirect(target_url: str, status_code: int = 307,
             headers: Optional[Mapping[str, str]] = None,
             background: Optional[BackgroundTask] = None, app_info: AppInfo = None) -> RedirectResponse:
    """重定向"""
    return RedirectResponse(target_url, status_code=status_code, headers=headers, background=background)
