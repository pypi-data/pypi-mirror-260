import asyncio
import traceback
from typing import Callable

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from starlette.requests import Request

from afeng_tools.application_tool.application_models import AppInfo
from afeng_tools.exception_tools.common_exception import AfengException, HttpException
from afeng_tools.fastapi_tool import fastapi_response_tools, fastapi_settings, fastapi_request_tools
from afeng_tools.fastapi_tool.core.fastapi_enums import FastapiConfigKeyEnum


def register_exception_handler(app: FastAPI, app_dict: dict[str, AppInfo] = None):
    """注册捕获全局异常"""

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常
        :param request: 请求头信息
        :param exc: 异常对象
        :return:
        """
        app_info = fastapi_request_tools.get_request_app_info(request, app_dict)
        # 日志记录异常详细上下文
        logger.error(
            f"[{request.url}]全局异常: \n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return fastapi_response_tools.resp_404(message="请求参数未找到！", request=request, app_info=app_info)

    @app.exception_handler(AfengException)
    async def afeng_exception_handler(request: Request, exc: AfengException):
        """
        自定义异常处理
        :param request: 请求头信息
        :param exc: 异常对象
        :return:
        """
        app_info = fastapi_request_tools.get_request_app_info(request, app_dict)
        # 日志记录异常详细上下文
        logger.error(
            f"[{request.url}]全局异常: \n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return fastapi_response_tools.resp_501(message=exc.message, request=request, app_info=app_info)

    @app.exception_handler(HttpException)
    async def http_exception_handler(request: Request, exc: HttpException):
        """
        http异常处理
        :param request: 请求头信息
        :param exc: 异常对象
        :return:
        """
        app_info = fastapi_request_tools.get_request_app_info(request, app_dict)
        # 日志记录异常详细上下文
        logger.error(
            f"[{request.url}]全局异常: \n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        if exc.status_code == 400:
            return fastapi_response_tools.resp_404(message=exc.message, request=request, app_info=app_info)
        elif exc.status_code == 501:
            return fastapi_response_tools.resp_501(message=exc.message, request=request, app_info=app_info)
        return fastapi_response_tools.resp_500(message=exc.message, request=request, app_info=app_info)

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        traceback_msg = traceback.format_exc()
        app_info = fastapi_request_tools.get_request_app_info(request, app_dict)
        if app_info:
            background_work_func = app_info.error500_background_work_func
        else:
            background_work_func = fastapi_settings.get_config(FastapiConfigKeyEnum.error500_background_work_func)
        if background_work_func and isinstance(background_work_func, Callable):
            asyncio.ensure_future(background_work_func(request, exc, traceback_msg))
        logger.error(
            f"全局异常: \n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback_msg}", exc)
        return fastapi_response_tools.resp_500(message="服务器内部错误", request=request, app_info=app_info)
