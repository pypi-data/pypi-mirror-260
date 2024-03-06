from napalm.package.detector_info import DetectorInfo, CompetitionInfo
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification

def _classification_to_str(classification: DetectorClassification) -> str:
    match classification:
        case DetectorClassification.HIGH:
            return "HIGH"
        case DetectorClassification.MEDIUM:
            return "MEDIUM"
        case DetectorClassification.LOW:
            return "LOW"
        case DetectorClassification.INFORMATIONAL:
            return "INFO"
        case DetectorClassification.OPTIMIZATION:
            return "OPTIMIZATION"
        case _:
            return "unknown"


def into_detector_info(slither_detector: AbstractDetector) -> DetectorInfo:
    severity = _classification_to_str(slither_detector.IMPACT)
    confidence = _classification_to_str(slither_detector.CONFIDENCE)

    competitors = (
        [
            CompetitionInfo(
                name=competitor.get("name"),
                title=competitor.get("title"),
            )
            for competitor in slither_detector.COMPETITORS
        ]
        if hasattr(slither_detector, "COMPETITORS")
        else []
    )

    return DetectorInfo(
        id=slither_detector.ARGUMENT or slither_detector.__name__,
        name=slither_detector.ARGUMENT or slither_detector.__name__,
        short_description=slither_detector.HELP or "No description available",
        long_description=slither_detector.HELP or "No description available",
        severity=severity,
        confidence=confidence,
        base=slither_detector,
        twins=[] if not hasattr(slither_detector, "TWINS") else slither_detector.TWINS,
        false_positive_prompt=(
            slither_detector.FALSE_POSITIVE_PROMPT
            if hasattr(slither_detector, "FALSE_POSITIVE_PROMPT")
            else None
        ),
        competitors=competitors,
    )
