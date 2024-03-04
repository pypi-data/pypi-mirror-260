from typing import Any

from afeng_tools.fastapi_tool.common.po_service.po_service import PoService


class LinkPoService(PoService):
    """
    使用示例：link_po_service = LinkPoService(app_info.db_code, LinkInfoPo)
    """

    def query_by_category_code(self, category_code: int) -> list[Any]:
        return self.query_more(self.model_type.category_code == category_code)

    def query_in_category_code(self, category_code_list: list[int]) -> list[Any]:
        return self.query_more(self.model_type.category_code.in_(category_code_list))

