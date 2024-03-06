from typing import Any

from afeng_tools.id_code_tool import id_code_tools
from afeng_tools.sqlalchemy_tools.core.sqlalchemy_enums import SortTypeEnum
from afeng_tools.sqlalchemy_tools.crdu import base_crdu
from sqlalchemy.orm import Query


class PoService:

    def __init__(self, db_code: str, model_type: type):
        self.db_code = db_code
        self.model_type = model_type

    def add(self, po) -> Any:
        return base_crdu.add(po, db_code=self.db_code)

    def add_batch(self, model_list: list[Any]) -> list:
        return base_crdu.add_all(model_list, db_code=self.db_code)

    def update(self, po, *criterion):
        return base_crdu.update(po, *criterion, db_code=self.db_code)

    def update_batch(self, model_list: list):
        return base_crdu.update_batch(model_list, db_code=self.db_code)

    def save(self, po, *criterion, auto_code: bool = False) -> Any:
        po = base_crdu.save(po, *criterion, db_code=self.db_code)
        if auto_code:
            if po.code is None:
                po.code = id_code_tools.get_code_by_id(po.id)
                po = base_crdu.update(po, db_code=self.db_code)
        return po

    def save_batch(self, model_list: list, *criterion, exist_update: bool = True) -> list:
        return base_crdu.save_batch(model_list, *criterion, exist_update=exist_update, db_code=self.db_code)

    def delete(self, *criterion):
        return base_crdu.delete(self.model_type, *criterion, db_code=self.db_code)

    def create_query(self, *criterion) -> Query:
        return base_crdu.create_query(self.model_type, *criterion, db_code=self.db_code)

    def get(self, *criterion) -> Any:
        return base_crdu.query_one(self.model_type, *criterion, db_code=self.db_code)

    def query_more(self, *criterion, sort_column: str = 'order_num',
                   sort_type: SortTypeEnum = SortTypeEnum.desc) -> list:
        return base_crdu.query_all(self.model_type, *criterion, sort_column=sort_column, sort_type=sort_type,
                                   db_code=self.db_code)

    def query_page(self, page_num, page_size, *criterion,
                   sort_column: str = 'order_num', sort_type: SortTypeEnum = SortTypeEnum.desc) -> list:
        return base_crdu.query_page(self.model_type, page_num, page_size, *criterion,
                                    sort_column=sort_column, sort_type=sort_type,
                                    db_code=self.db_code)

    def count(self, *criterion) -> int:
        return base_crdu.query_page(self.model_type, *criterion, db_code=self.db_code)
