from janus.constants.FileTag import FileTag
from janus.services.parser import parse_sample_metrics, parse_fastp, parse_somalier


tag_to_parse_function: dict = {
    FileTag.HS_METRICS: parse_sample_metrics,
    FileTag.WGS_METRICS: parse_sample_metrics,
    FileTag.DUPLICATES: parse_sample_metrics,
    FileTag.INSERT_SIZE: parse_sample_metrics,
    FileTag.ALIGNMENT_SUMMARY_METRICS: parse_sample_metrics,
    FileTag.FASTP: parse_fastp,
    FileTag.SOMALIER: parse_somalier,
    FileTag.SAMTOOLS_STATS: parse_sample_metrics,
}
