class BaseService:
    po_service_type: type = None

    def __init__(self, db_code: str, po_model_type: type, app_code: str = None):
        self.app_code = app_code
        self.db_code = db_code
        self.po_model_type = po_model_type
        if self.po_service_type:
            self.po_service = self.po_service_type(self.db_code, self.po_model_type)
