from __future__ import annotations

from typing import Optional


def detect_language(text: str | None) -> Optional[str]:
    if not text or len(text.strip()) < 20:
        return None
    try:
        from langdetect import DetectorFactory, LangDetectException, detect
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "langdetect is required for README language detection. Install project dependencies first."
        ) from exc

    DetectorFactory.seed = 0
    try:
        return detect(text)
    except LangDetectException:
        return None
