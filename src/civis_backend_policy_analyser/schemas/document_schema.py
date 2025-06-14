from datetime import datetime
from typing import Optional

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema

class DocumentBase(BaseModelSchema):
    doc_id: str
    file_name: str
    file_type: str
    upload_time: datetime
    number_of_pages: int
    doc_size_kb: int

class DocumentOut(DocumentBase):
    warning: Optional[str] = None
    new_document: Optional["DocumentBase"] = None


    class Config:
        orm_mode = True
