"""Text-processing helpers for LLM output."""

import re

_EMOJI_PATTERN = re.compile(
    "["
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f680-\U0001f6ff"  # transport
    "\U0001f700-\U0001f7ff"  # geometric
    "\U0001f900-\U0001f9ff"  # supplemental
    "\U0001fa00-\U0001faff"  # extended pictographs
    "\U00002600-\U000026ff"  # misc symbols
    "\U00002700-\U000027bf"  # dingbats
    "\U0001f1e6-\U0001f1ff"  # regional indicators (flags)
    "\U0000fe0f"  # variation selector-16
    "\U0000200d"  # zero-width joiner
    "]",
    flags=re.UNICODE,
)


def strip_emojis(text: str) -> str:
    """Remove emoji characters from text. Safety net for LLM output."""
    return _EMOJI_PATTERN.sub("", text)
