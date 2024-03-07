from enum import StrEnum


class FileTag(StrEnum):
    """File tags."""

    HS_METRICS: str = "picard-hs"
    WGS_METRICS: str = "picard-wgs"
    DUPLICATES: str = "picard-duplicates"
    INSERT_SIZE: str = "picard-insert-size"
    ALIGNMENT_SUMMARY_METRICS: str = "picard-alignment"
    FASTP: str = "fastp"
    SOMALIER: str = "somalier"
    SAMTOOLS_STATS: str = "samtools-stats"
