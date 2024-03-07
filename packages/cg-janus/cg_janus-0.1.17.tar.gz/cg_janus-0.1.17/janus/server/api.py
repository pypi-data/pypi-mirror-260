from http import HTTPStatus

from fastapi import APIRouter, Body
from starlette.responses import JSONResponse

from janus.dto.collect_qc_request import CollectQCRequest
from janus.dto.collect_qc_response import CollectQCResponse
from janus.exceptions.exceptions import WorkflowNotSupportedError
from janus.services.collect_qc_service import CollectQCService
from pydantic import ValidationError

collect_qc_router = APIRouter()


@collect_qc_router.post(
    "/collect_qc/",
    response_description="Collect qc metrics for a case.",
    response_model=CollectQCResponse,
)
def collect_qc(collect_request: CollectQCRequest = Body(...)) -> str | JSONResponse:
    """Collect qc metrics for the external request."""
    service = CollectQCService(collect_request)
    try:
        collected_qc_metrics: CollectQCResponse = service.collect_qc_metrics_for_request()
        return collected_qc_metrics.model_dump_json()
    except (ValueError, FileNotFoundError, ValidationError, WorkflowNotSupportedError) as error:
        return JSONResponse(content=repr(error), status_code=HTTPStatus.BAD_REQUEST)
