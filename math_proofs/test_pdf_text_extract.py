from __future__ import annotations

import tempfile
import unittest
import zlib
from pathlib import Path

from math_proofs.pdf_text_extract import extract_pdf_text_lines


def _build_minimal_pdf(stream_payload: bytes) -> bytes:
    compressed = zlib.compress(stream_payload)
    header = b"%PDF-1.4\n"
    obj = (
        b"1 0 obj\n"
        + f"<< /Length {len(compressed)} /Filter /FlateDecode >>\n".encode("ascii")
        + b"stream\n"
        + compressed
        + b"\nendstream\nendobj\n"
    )
    return header + obj + b"%%EOF\n"


class PdfTextExtractTests(unittest.TestCase):
    def _extract(self, stream_payload: bytes) -> list[str]:
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = Path(tmpdir) / "sample.pdf"
            pdf_path.write_bytes(_build_minimal_pdf(stream_payload))
            return extract_pdf_text_lines(pdf_path, max_lines=50)

    def test_extracts_tj_literal(self) -> None:
        lines = self._extract(b"BT /F1 12 Tf 72 720 Td (Hello Steiner) Tj ET")
        self.assertTrue(any("Hello Steiner" in line for line in lines))

    def test_extracts_tj_array(self) -> None:
        lines = self._extract(b"BT [(Steiner) 120 ( Systems)] TJ ET")
        self.assertTrue(any("Steiner Systems" in line for line in lines))

    def test_extracts_escaped_literal(self) -> None:
        lines = self._extract(b"BT (A\\(B\\)\\040C) Tj ET")
        self.assertTrue(any("A(B) C" in line for line in lines))


if __name__ == "__main__":
    unittest.main()
