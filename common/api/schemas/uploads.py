from datetime import datetime

from pydantic import BaseModel

from ...domain.models.upload import UploadStatus


class SUpload(BaseModel):
    upload_id: int
    uploaded_at: datetime
    status: UploadStatus
    filename: str
    has_validation: bool


class SUploadCreate(BaseModel):
    has_validation: bool


class SUploadProcessingProgress(BaseModel):
    total_texts: int
    processed_texts: int
