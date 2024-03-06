from typing import Any

from afeng_tools.fastapi_tool.common.po_service.po_service import PoService


class GroupPoService(PoService):
    """
    使用示例：group_po_service = GroupPoService(app_info.db_code, GroupInfoPo)
    """

    def get_group(self, title: str, app_code: str, type_code: str) -> Any:
        group_po = self.get(self.model_type.title == title,
                            self.model_type.app_code == app_code, self.model_type.type_code == type_code)
        if not group_po:
            group_po = self.save(self.model_type(
                title=title,
                app_code=app_code,
                type_code=type_code
            ), auto_code=True)
        return group_po
