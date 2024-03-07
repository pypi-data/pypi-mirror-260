from enum import Enum

from janus.constants.FileTag import FileTag
from janus.models.multiqc.models import (
    PicardHsMetrics,
    PicardWGSMetrics,
    PicardDuplicates,
    PicardInsertSize,
    PicardAlignmentSummary,
    Fastp,
    Somalier,
    SamtoolsStats,
)


tag_to_model = {
    FileTag.HS_METRICS: PicardHsMetrics,
    FileTag.WGS_METRICS: PicardWGSMetrics,
    FileTag.DUPLICATES: PicardDuplicates,
    FileTag.INSERT_SIZE: PicardInsertSize,
    FileTag.FASTP: Fastp,
    FileTag.ALIGNMENT_SUMMARY_METRICS: PicardAlignmentSummary,
    FileTag.SOMALIER: Somalier,
    FileTag.SAMTOOLS_STATS: SamtoolsStats,
}
