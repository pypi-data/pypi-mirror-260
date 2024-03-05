from pydantic import BaseModel

from janus.models.workflow.balsamic import Balsamic


class CollectQCResponse(BaseModel):
    """Collect QC response model."""

    case_id: str
    case_info: Balsamic
