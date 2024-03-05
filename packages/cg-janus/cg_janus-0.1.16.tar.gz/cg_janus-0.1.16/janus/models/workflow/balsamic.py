"""Module for the workflow models."""

from pydantic import BaseModel, Field

from janus.constants.FileTag import FileTag
from janus.dto.collect_qc_request import WorkflowInfo
from janus.models.multiqc.models import (
    Somalier,
    PicardAlignmentSummary,
    PicardDuplicates,
    PicardHsMetrics,
    PicardInsertSize,
    PicardWGSMetrics,
    SamtoolsStats,
    Fastp,
)


class BalsamicSample(BaseModel):
    sample_id: str
    alignment_summary_metrics: PicardAlignmentSummary | None = Field(
        ..., alias=FileTag.ALIGNMENT_SUMMARY_METRICS
    )
    duplicates: PicardDuplicates = Field(..., alias=FileTag.DUPLICATES)
    wgs_metrics: PicardWGSMetrics | None = Field(..., alias=FileTag.WGS_METRICS)
    hs_metrics: PicardHsMetrics = Field(..., alias=FileTag.HS_METRICS)
    insert_size: PicardInsertSize = Field(..., alias=FileTag.INSERT_SIZE)
    samtools_stats: SamtoolsStats = Field(..., alias=FileTag.SAMTOOLS_STATS)
    fastp: Fastp = Field(..., alias=FileTag.FASTP)


class Balsamic(BaseModel):
    samples: list[BalsamicSample]
    somalier: Somalier | None
    workflow: WorkflowInfo
