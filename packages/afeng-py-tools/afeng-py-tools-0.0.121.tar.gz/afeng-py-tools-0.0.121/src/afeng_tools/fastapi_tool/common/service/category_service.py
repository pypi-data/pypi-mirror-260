from typing import Any

from afeng_tools.fastapi_tool.common.po_service.category_po_service import CategoryPoService
from afeng_tools.fastapi_tool.common.service.base_service import BaseService


class CategoryService(BaseService):
    """
    使用示例：category_service = CategoryService(app_info.db_code, CategoryInfoPo)
    """

    po_service_type = CategoryPoService

    def _up_tree_category(self, category_code: int, category_dict: dict[int, Any]) -> list[Any]:
        """向上获取递归获取分类信息"""
        category_list = []
        tmp_category = category_dict.get(category_code)
        if tmp_category.parent_code:
            category_list.extend(self._up_tree_category(tmp_category.parent_code, category_dict))
        category_list.append(tmp_category)
        return category_list

    def _down_tree_category(self, category_code: int, category_dict: dict[int, Any],
                            recursion: bool = False) -> list[Any]:
        """
        向下获取递归获取分类信息， 第一项是当前分类
        :param category_code:
        :param category_dict:
        :param recursion: 是否层级递归
        :return:
        """
        category_list = []
        tmp_category = category_dict.get(category_code)
        category_list.append(tmp_category)
        for tmp_po in category_dict.values():
            if tmp_po.parent_code == category_code:
                category_list.append(tmp_po)
                if recursion:
                    category_list.extend(self._down_tree_category(tmp_po.code, category_dict, recursion=recursion))
        return category_list

    def get_category_list(self, category_code: int, group_code: int = None, up: bool = True) -> list[Any]:
        """
        通过分类编码获取分类列表: 如：['程序开发','Java','Java虚拟机']
        :param group_code: 分组编码
        :param category_code:
        :param up:
            当为True时，向上获取，如当前是Java虚拟机,获取到的是['程序开发','Java','Java虚拟机']
            当为False时，向下获取，如当前是Java,获取到的是['Java基础','Java安全','Java虚拟机', ,'JavaWeb开发']
        :return: 分类列表
        """
        if group_code is None:
            category_info = self.po_service.get_one(self.po_model_type.code == category_code)
            group_code = category_info.group_code
        category_dict = {tmp.code: tmp for tmp in self.po_service.query_group_data(group_code)}
        return self._up_tree_category(category_code, category_dict) if up else self._down_tree_category(category_code,
                                                                                                        category_dict)

    def get_up_category_title_list(self, category_code: int, group_code: int = None) -> list[str]:
        """获取向上的分类标题"""
        category_list = self.get_category_list(group_code=group_code, category_code=category_code, up=True)
        return [tmp.title for tmp in category_list]
