"""Post request model for JanusAPI."""

from pydantic import BaseModel


class WorkflowInfo(BaseModel):
    workflow: str
    version: str


class FilePathAndTag(BaseModel):
    """Model for the file path and its associated tag."""

    file_path: str
    tag: str


class CollectQCRequest(BaseModel):
    """Model for the qc collection request."""

    case_id: str
    sample_ids: list[str]
    files: list[FilePathAndTag]
    workflow_info: WorkflowInfo
