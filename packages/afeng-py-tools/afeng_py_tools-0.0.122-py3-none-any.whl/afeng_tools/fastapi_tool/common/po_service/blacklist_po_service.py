from typing import Any

from afeng_tools.sqlalchemy_tools.crdu import base_crdu

from afeng_tools.cache_tool.cache_decorator import cache_with_expiration
from afeng_tools.fastapi_tool.common.po_service.po_service import PoService


class BlacklistPoService(PoService):
    """
    使用示例：blacklist_po_service = BlacklistPoService(app_info.db_code,BlacklistInfoPo)
    """
    def query_by_type_code(self, type_code: str) -> list[Any]:
        return base_crdu.query_all(self.model_type,
                                   self.model_type.type_code == type_code,
                                   db_code=self.db_code)

    @cache_with_expiration(expiration=3600 * 2)
    def query_weixin_black_list(self):
        """查询微信黑名单"""
        data_list = self.query_by_type_code('wx_blacklist')
        return [tmp.type_value for tmp in data_list] if data_list else []

    @cache_with_expiration(expiration=3600 * 24)
    def query_ip_black_list(self):
        """查询ip黑名单"""
        data_list = self.query_by_type_code('ip_blacklist')
        return [tmp.type_value for tmp in data_list] if data_list else []

