from pydantic import BaseModel
from enum import Enum
from typing import Optional

class ModelEnum(str, Enum):
    gpt_4o = "gpt-4o"
    gpt_4o_mini = "gpt-4o-mini"

class QueryInput(BaseModel):
    question: str
    session_id: Optional[str] = None
    model: ModelEnum = ModelEnum.gpt_4o

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelEnum

class DocumentInfo(BaseModel):
    file_id: str
    filename: str

class DeleteFileRequest(BaseModel):
    file_id: str
