"""Handler for the expense_ocr_extract tool — interface contract (placeholder).

Shape: read-external / paid / no-local-write.
  - Makes a paid outbound network call to an external OCR API.
  - Returns the raw extracted text as a string.
  - Writes NOTHING to disk or to ledger.db (no local side effect).

Path-traversal note (general security convention, not business logic):
  Validate that file_path is within the designated input root before sending to
  OCR. Use Path.is_relative_to (py3.9+), NOT str.startswith: for root /inbox,
  the path /inbox-evil/x shares the textual prefix "/inbox" and would pass
  startswith while actually living outside the root. is_relative_to compares
  path components and correctly rejects /inbox-evil.

Business implementation: connect your OCR provider here (e.g. Google Document
AI, AWS Textract, a custom HTTP endpoint). The harness does not prescribe the
provider, request format, or response parsing.
"""

from __future__ import annotations


def ocr_extract(file_path: str) -> str:
    """Return raw OCR text for one invoice/receipt file.

    When to call (mirrors inputSchema description): call once per source
    document before any field extraction. Do NOT call on a file already
    OCR'd in this turn.

    Args:
        file_path: Absolute path to the invoice/receipt file (.pdf, .png,
                   .jpg, or .txt). Must be a path the agent was given as
                   input; do not synthesize or guess paths.

    Returns:
        Raw text extracted from the document.

    Raises:
        ValueError: If file_path is outside the allowed input root.
        FileNotFoundError: If the file does not exist.
        NotImplementedError: Until a real OCR provider is wired in.
    """
    raise NotImplementedError(
        "接入你的业务逻辑; harness 不规定 OCR provider 或请求格式。"
        " 实现应: 1) 校验 file_path 在允许根目录内(用 Path.is_relative_to), "
        "2) 调外部 OCR API, 3) 返回原始文本字符串。"
    )
