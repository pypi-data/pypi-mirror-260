"""Module to hold the collect qc service."""

from janus.constants.FileTag import FileTag
from janus.constants.workflow import Workflow
from janus.dto.collect_qc_request import CollectQCRequest
from janus.dto.collect_qc_response import CollectQCResponse
from janus.exceptions.exceptions import WorkflowNotSupportedError
from janus.mappers.tag_to_parse_function import tag_to_parse_function
from janus.models.workflow.balsamic import Balsamic


class CollectQCService:
    def __init__(self, collect_qc_request):
        self.request: CollectQCRequest = collect_qc_request

    def collect_metrics(self) -> list[dict]:
        """Collect the metrics for the files provided in the request."""
        collected_metrics: list[callable] = []
        for file_path_and_tag in self.request.files:
            parse_function = tag_to_parse_function[file_path_and_tag.tag]
            collected_metrics.append(
                parse_function(
                    file_path=file_path_and_tag.file_path,
                    sample_ids=self.request.sample_ids,
                    tag=file_path_and_tag.tag,
                    case_id=self.request.case_id,
                )
            )
        return collected_metrics

    @staticmethod
    def format_sample_metrics(collected_metrics: list[dict], sample_id: str) -> dict:
        """Format the metrics for a sample."""
        sample_metrics: dict = {"sample_id": sample_id}
        for collected_metric in collected_metrics:
            for sample, metric in collected_metric.items():
                if sample == sample_id:
                    sample_metrics.update(metric)
        return sample_metrics

    def get_formatted_sample_metrics(
        self, collected_metrics: list[dict], sample_ids: list[str]
    ) -> list:
        """Get formatted sample metrics."""
        formatted_sample_metrics: list = []
        for sample_id in sample_ids:
            collected_sample_metrics: dict = self.format_sample_metrics(
                collected_metrics=collected_metrics, sample_id=sample_id
            )
            formatted_sample_metrics.append(collected_sample_metrics)
        return formatted_sample_metrics

    @staticmethod
    def get_case_metrics(collected_metrics: list[dict], case_id: str) -> dict:
        """Get case metrics."""
        case_metrics: list = []
        for metric in collected_metrics:
            for key in metric.keys():
                if key == case_id:
                    case_metrics.append(metric[key])
        return {case_id: case_metrics}

    @staticmethod
    def extract_somalier(case_metrics: dict) -> dict:
        """Extract somalier metrics from case metrics."""
        for metric in case_metrics:
            somalier = metric[FileTag.SOMALIER]
            if not somalier:
                raise ValueError("No Somalier entry found.")
            return somalier

    def collect_balsamic_metrics(self) -> Balsamic:
        """Collect multiqc metrics for balsamic workflow."""
        collected_metrics: list[dict] = self.collect_metrics()
        sample_metrics: list = self.get_formatted_sample_metrics(
            collected_metrics=collected_metrics, sample_ids=self.request.sample_ids
        )
        case_metrics: dict = self.get_case_metrics(
            collected_metrics=collected_metrics, case_id=self.request.case_id
        )
        somalier = self.extract_somalier(case_metrics[self.request.case_id])
        return Balsamic(
            samples=sample_metrics,
            somalier=somalier,
            workflow=self.request.workflow_info,
        )

    def get_case_info_for_workflow(self) -> callable:
        """Return the collect function for the workflow."""
        case_info_workflow_collector = {
            Workflow.BALSAMIC: self.collect_balsamic_metrics(),
            Workflow.BALSAMIC_QC: self.collect_balsamic_metrics(),
            Workflow.BALSAMIC_UMI: self.collect_balsamic_metrics(),
        }
        return case_info_workflow_collector[self.request.workflow_info.workflow]

    def is_supported_workflow(self):
        return self.request.workflow_info.workflow in Workflow.values()

    def collect_qc_metrics_for_request(self) -> CollectQCResponse:
        """Collect the qc metrics requested by the external source."""
        if not self.is_supported_workflow():
            raise WorkflowNotSupportedError(
                f"Janus does not support parsing of qc metrics for {self.request.workflow_info.workflow})"
            )
        case_info: callable = self.get_case_info_for_workflow()
        qc_metrics = CollectQCResponse(case_id=self.request.case_id, case_info=case_info)
        return qc_metrics
