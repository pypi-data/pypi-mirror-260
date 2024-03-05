"""Module that holds the parsing functionality."""

from enum import Enum
from itertools import product
from pathlib import Path

from janus.constants.FileTag import FileTag
from janus.io.read_json import read_json
from janus.mappers.tag_to_models import tag_to_model

from janus.models.multiqc.models import (
    PicardInsertSize,
    SamtoolsStats,
    PicardHsMetrics,
    PicardAlignmentSummary,
    SomalierIndividual,
    SomalierComparison,
    Somalier,
    Fastp,
    FastpAfterFiltering,
    FastpBeforeFiltering,
)


def parse_sample_metrics(
    file_path: Path, sample_ids: list[str], tag: str, **kwargs
) -> dict[SamtoolsStats | PicardHsMetrics | PicardInsertSize | PicardAlignmentSummary]:
    """Parse the content for a given file path into the corresponding model for each sample."""
    json_content: list[dict] = read_json(file_path)
    parsed_content: dict[
        SamtoolsStats | PicardHsMetrics | PicardInsertSize | PicardAlignmentSummary
    ] = {}
    for entry, sample_id in product(json_content, sample_ids):
        if sample_id in entry:
            parsed_content[sample_id] = {tag: tag_to_model[tag](**json_content[entry])}
    return parsed_content


def parse_somalier(file_path: Path, case_id: str, **kwargs) -> dict[str, Somalier]:
    """Parse the somalier multiqc file."""
    individuals: list[SomalierIndividual] = []
    comparison: SomalierComparison | None = None
    json_content: list[dict] = read_json(file_path)

    for entry in json_content:
        if entry.__contains__("*"):
            comparison = SomalierComparison(**json_content[entry])
        else:
            individuals.append(SomalierIndividual(**json_content[entry]))
    somalier_content: dict = {
        FileTag.SOMALIER: Somalier(individual=individuals, comparison=comparison)
    }
    return {case_id: somalier_content}


def parse_fastp(file_path: Path, sample_ids: list[str], **kwargs) -> dict[Fastp]:
    """Parse the Fastp multiqc file."""
    json_content: list[dict] = read_json(file_path)
    parsed_content: dict[Fastp] = {}
    for entry, sample_id in product(json_content, sample_ids):
        if sample_id in entry:
            before_filtering = FastpBeforeFiltering(
                **json_content[entry]["summary"]["before_filtering"]
            )
            after_filtering = FastpAfterFiltering(
                **json_content[entry]["summary"]["after_filtering"]
            )
            parsed_content[sample_id] = {
                FileTag.FASTP: Fastp(
                    before_filtering=before_filtering, after_filtering=after_filtering
                )
            }

    return parsed_content
