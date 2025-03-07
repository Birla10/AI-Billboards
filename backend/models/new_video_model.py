from pydantic import BaseModel
from typing import Set
from fastapi import UploadFile

class NewVideoModel(BaseModel):
    file: UploadFile
    keywords: Set[str]