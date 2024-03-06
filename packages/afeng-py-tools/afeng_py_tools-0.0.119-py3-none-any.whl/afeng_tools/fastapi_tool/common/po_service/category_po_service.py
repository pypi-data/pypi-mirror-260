from typing import Any

from afeng_tools.fastapi_tool.common.po_service.po_service import PoService
from afeng_tools.sqlalchemy_tools.crdu import base_crdu


class CategoryPoService(PoService):
    """
    使用示例：category_po_service = CategoryPoService(app_info.db_code, CategoryInfoPo)
    """

    def get_category(self, title: str, group_code: int, parent_code: int = None) -> Any:
        category_po = self.get(self.model_type.title == title,
                               self.model_type.group_code == group_code, self.model_type.parent_code == parent_code)
        if not category_po:
            category_po = self.save(self.model_type(
                group_code=group_code,
                parent_code=parent_code,
                title=title
            ), auto_code=True)
        return category_po

    def query_all_data(self, group_code: int = None) -> list:
        """查询所有数据"""
        if group_code:
            return base_crdu.query_all(self.model_type, self.model_type.group_code == group_code, db_code=self.db_code)
        else:
            return base_crdu.query_all(self.model_type, db_code=self.db_code)

    def query_all_data_dict(self, group_code: int = None) -> dict[int, Any]:
        """
        查询所有数据字典(code为键)
        :return: {code: BookCategoryPo}
        """
        return {tmp.code: tmp for tmp in self.query_all_data(group_code)}

    def query_group_data_dict(self) -> dict[int, list[Any]]:
        """
        查询分组数据字典(group_code为键)
        :return: {group_code: BookCategoryPo}
        """
        data_list = self.query_all_data()
        result_dict = dict()
        for tmp in data_list:
            if not result_dict.get(tmp.group_code):
                result_dict[tmp.group_code] = []
            result_dict[tmp.group_code].append(tmp)
        return result_dict

    def query_group_data(self, group_code: int,
                         category_dict: dict[int, list[Any]] = None) -> list[Any]:
        """
        查询某个分组的类别数据
        :param group_code: 分组编码
        :param category_dict: 类别字典：{group_code: BookCategoryPo}
        :return:
        """
        if category_dict:
            return category_dict.get(group_code)
        else:
            return base_crdu.query_all(self.model_type, self.model_type.group_code == group_code,
                                       db_code=self.db_code)
