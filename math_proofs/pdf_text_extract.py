from __future__ import annotations

import argparse
import base64
import json
import re
import zlib
from pathlib import Path
from typing import Iterable


STREAM_HEADER_RE = re.compile(rb"<<(?P<dict>.*?)>>\s*stream\r?\n", re.DOTALL)
FILTER_RE = re.compile(rb"/Filter\s*(?P<value>\[[^\]]+\]|/[A-Za-z0-9]+)")
NAME_RE = re.compile(rb"/([A-Za-z0-9]+)")
BT_ET_RE = re.compile(rb"BT(.*?)ET", re.DOTALL)
ASCII_RUN_RE = re.compile(rb"[ -~]{30,}")
TITLE_HEX_RE = re.compile(rb"/Title\s*<([0-9A-Fa-f]+)>")
URL_RE = re.compile(rb"https?://[^\s<>()\"']+")


def _parse_filters(dict_blob: bytes) -> list[str]:
    match = FILTER_RE.search(dict_blob)
    if not match:
        return []
    raw = match.group("value").strip()
    if raw.startswith(b"["):
        return [name.decode("ascii", errors="ignore") for name in NAME_RE.findall(raw)]
    if raw.startswith(b"/"):
        return [raw[1:].decode("ascii", errors="ignore")]
    return []


def _ascii_hex_decode(data: bytes) -> bytes | None:
    payload = re.sub(rb"\s+", b"", data)
    if payload.endswith(b">"):
        payload = payload[:-1]
    if len(payload) % 2 == 1:
        payload += b"0"
    try:
        return bytes.fromhex(payload.decode("ascii"))
    except Exception:
        return None


def _ascii85_decode(data: bytes) -> bytes | None:
    payload = data.strip()
    if not payload:
        return b""
    if not payload.startswith(b"<~"):
        payload = b"<~" + payload
    if not payload.endswith(b"~>"):
        payload = payload + b"~>"
    try:
        return base64.a85decode(payload, adobe=True, ignorechars=b" \t\r\n\x0b\x0c")
    except Exception:
        return None


def _flate_decode(data: bytes) -> bytes | None:
    for wbits in (zlib.MAX_WBITS, -zlib.MAX_WBITS):
        try:
            return zlib.decompress(data, wbits)
        except Exception:
            continue
    return None


def _apply_filters(raw: bytes, filters: list[str]) -> bytes | None:
    data = raw
    for flt in filters:
        name = flt.lower()
        if name in {"flatedecode", "fl"}:
            data = _flate_decode(data)
        elif name in {"ascii85decode", "a85"}:
            data = _ascii85_decode(data)
        elif name in {"asciihexdecode", "ahx"}:
            data = _ascii_hex_decode(data)
        else:
            return None
        if data is None:
            return None
    return data


def _iter_decoded_streams(pdf_bytes: bytes) -> Iterable[bytes]:
    for match in STREAM_HEADER_RE.finditer(pdf_bytes):
        dict_blob = match.group("dict")
        start = match.end()
        end = pdf_bytes.find(b"endstream", start)
        if end == -1:
            continue
        raw = pdf_bytes[start:end]
        if raw.endswith(b"\r\n"):
            raw = raw[:-2]
        elif raw.endswith(b"\n") or raw.endswith(b"\r"):
            raw = raw[:-1]
        filters = _parse_filters(dict_blob)
        decoded = _apply_filters(raw, filters)
        if decoded is None:
            # Best-effort fallback for mislabeled streams.
            decoded = _flate_decode(raw)
        if decoded:
            yield decoded


def _read_pdf_literal(data: bytes, index: int) -> tuple[bytes, int]:
    # data[index] must be b'('
    out = bytearray()
    i = index + 1
    depth = 1
    while i < len(data):
        byte = data[i]
        if byte == 0x5C:  # backslash escape
            i += 1
            if i >= len(data):
                break
            esc = data[i]
            mapping = {
                ord("n"): b"\n",
                ord("r"): b"\r",
                ord("t"): b"\t",
                ord("b"): b"\b",
                ord("f"): b"\f",
                ord("("): b"(",
                ord(")"): b")",
                ord("\\"): b"\\",
            }
            if esc in mapping:
                out.extend(mapping[esc])
                i += 1
                continue
            if esc in (ord("\r"), ord("\n")):
                if esc == ord("\r") and i + 1 < len(data) and data[i + 1] == ord("\n"):
                    i += 2
                else:
                    i += 1
                continue
            if 48 <= esc <= 55:
                digits = [esc]
                for _ in range(2):
                    if i + 1 < len(data) and 48 <= data[i + 1] <= 55:
                        i += 1
                        digits.append(data[i])
                    else:
                        break
                out.append(int(bytes(digits), 8))
                i += 1
                continue
            out.append(esc)
            i += 1
            continue

        if byte == 0x28:  # '('
            depth += 1
            out.append(byte)
            i += 1
            continue
        if byte == 0x29:  # ')'
            depth -= 1
            if depth == 0:
                return bytes(out), i + 1
            out.append(byte)
            i += 1
            continue

        out.append(byte)
        i += 1
    return bytes(out), i


def _decode_pdf_bytes(raw: bytes) -> str:
    for encoding in ("utf-8", "latin1"):
        try:
            return raw.decode(encoding, errors="ignore")
        except Exception:
            continue
    return ""


def _skip_ws(data: bytes, index: int) -> int:
    i = index
    while i < len(data) and data[i] in b" \t\r\n\x0c\x00":
        i += 1
    return i


def _extract_literals_from_array(data: bytes) -> str:
    pieces: list[str] = []
    i = 0
    while i < len(data):
        if data[i] == ord("("):
            raw, next_i = _read_pdf_literal(data, i)
            decoded = _decode_pdf_bytes(raw)
            if decoded:
                pieces.append(decoded)
            i = next_i
            continue
        i += 1
    return "".join(pieces)


def _extract_text_ops(content: bytes) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(content):
        byte = content[i]
        if byte == ord("("):
            raw, next_i = _read_pdf_literal(content, i)
            j = _skip_ws(content, next_i)
            if content[j : j + 2] == b"Tj":
                decoded = _decode_pdf_bytes(raw)
                if decoded:
                    out.append(decoded)
            i = next_i
            continue

        if byte == ord("["):
            depth = 1
            j = i + 1
            while j < len(content):
                if content[j] == ord("("):
                    _, j = _read_pdf_literal(content, j)
                    continue
                if content[j] == ord("["):
                    depth += 1
                elif content[j] == ord("]"):
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j < len(content):
                k = _skip_ws(content, j + 1)
                if content[k : k + 2] == b"TJ":
                    decoded = _extract_literals_from_array(content[i + 1 : j])
                    if decoded:
                        out.append(decoded)
                i = j + 1
                continue

        if byte == ord("<") and i + 1 < len(content) and content[i + 1] != ord("<"):
            end = content.find(b">", i + 1)
            if end != -1:
                k = _skip_ws(content, end + 1)
                if content[k : k + 2] == b"Tj":
                    hex_blob = re.sub(rb"\s+", b"", content[i + 1 : end])
                    if len(hex_blob) % 2 == 1:
                        hex_blob += b"0"
                    try:
                        decoded = bytes.fromhex(hex_blob.decode("ascii"))
                    except Exception:
                        decoded = b""
                    text = _decode_pdf_bytes(decoded)
                    if text:
                        out.append(text)
                i = end + 1
                continue

        i += 1
    return out


def _normalize_line(text: str) -> str:
    cleaned = text.replace("\x00", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def _is_pdf_syntax_noise(line: str) -> bool:
    lower = line.lower()
    if not lower:
        return True
    if " " not in line and not lower.startswith("http"):
        return True
    if lower.startswith(("<<", "<</", "/cidinit", "endobj", "xref", "trailer", "startxref")):
        return True
    if "cmap defineresource" in lower or "noto sans cjk" in lower:
        return True
    if lower.startswith("/"):
        return True
    if re.match(r"^\d+\s+\d+\s+obj\b", lower):
        return True
    if re.match(r"^[0-9 .\-]+$", lower):
        return True
    if re.match(r"^[0-9 .\-]+tm$", lower):
        return True
    if "/type /annot" in lower or "/type /page" in lower or "/type /catalog" in lower:
        return True
    if lower.count("/") > 8 and "http" not in lower:
        return True
    return False


def extract_pdf_text_lines(
    pdf_path: Path, *, max_lines: int = 400, min_ascii_run_len: int = 30
) -> list[str]:
    pdf_bytes = pdf_path.read_bytes()
    decoded_streams = list(_iter_decoded_streams(pdf_bytes))
    combined = b"\n".join(decoded_streams)
    lines: list[str] = []
    seen: set[str] = set()

    for stream in decoded_streams:
        blocks = BT_ET_RE.findall(stream)
        if not blocks:
            blocks = [stream]
        for block in blocks:
            for candidate in _extract_text_ops(block):
                line = _normalize_line(candidate)
                if len(line) < 4:
                    continue
                if not re.search(r"[A-Za-z]", line):
                    continue
                if _is_pdf_syntax_noise(line):
                    continue
                key = line.lower()
                if key in seen:
                    continue
                seen.add(key)
                lines.append(line)
                if len(lines) >= max_lines:
                    return lines

    if len(lines) < max_lines:
        title_match = TITLE_HEX_RE.search(pdf_bytes) or TITLE_HEX_RE.search(combined)
        if title_match:
            try:
                title_raw = bytes.fromhex(title_match.group(1).decode("ascii"))
                if title_raw.startswith(b"\xfe\xff"):
                    title = title_raw[2:].decode("utf-16-be", errors="ignore")
                elif title_raw.startswith(b"\xff\xfe"):
                    title = title_raw[2:].decode("utf-16-le", errors="ignore")
                else:
                    title = title_raw.decode("latin1", errors="ignore")
                title = _normalize_line(title)
                if title and not _is_pdf_syntax_noise(title):
                    key = title.lower()
                    if key not in seen:
                        seen.add(key)
                        lines.append(f"Title: {title}")
            except Exception:
                pass
        if len(lines) >= max_lines:
            return lines

    if len(lines) < max_lines:
        for raw_url in URL_RE.findall(pdf_bytes) + URL_RE.findall(combined):
            try:
                url = raw_url.decode("latin1", errors="ignore")
            except Exception:
                continue
            url = _normalize_line(url)
            if not url:
                continue
            key = url.lower()
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"URL: {url}")
            if len(lines) >= max_lines:
                return lines

    # Fallback: capture plain ASCII runs from decoded streams.
    for stream in decoded_streams:
        for match in ASCII_RUN_RE.finditer(stream):
            if len(match.group(0)) < min_ascii_run_len:
                continue
            candidate = _normalize_line(match.group(0).decode("latin1", errors="ignore"))
            if len(candidate) < 20:
                continue
            if not re.search(r"[A-Za-z]{4,}", candidate):
                continue
            if _is_pdf_syntax_noise(candidate):
                continue
            key = candidate.lower()
            if key in seen:
                continue
            seen.add(key)
            lines.append(candidate)
            if len(lines) >= max_lines:
                return lines

    return lines


def extract_pdf_text(pdf_path: Path, *, max_lines: int = 400) -> str:
    return "\n".join(extract_pdf_text_lines(pdf_path, max_lines=max_lines))


def _cli_extract_file(pdf_path: Path, max_lines: int) -> int:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    print(extract_pdf_text(pdf_path, max_lines=max_lines))
    return 0


def _cli_extract_dir(pdf_dir: Path, output_dir: Path, max_lines: int) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary: list[dict[str, object]] = []
    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        lines = extract_pdf_text_lines(pdf_path, max_lines=max_lines)
        output_path = output_dir / f"{pdf_path.stem}.txt"
        output_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        summary.append(
            {
                "pdf": str(pdf_path),
                "output": str(output_path),
                "line_count": len(lines),
            }
        )
    print(json.dumps({"output_dir": str(output_dir), "files": summary}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Best-effort PDF text extraction for local research loops."
    )
    parser.add_argument(
        "input",
        help="PDF file path or directory containing PDFs.",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Directory for extracted .txt outputs when input is a directory.",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=400,
        help="Maximum lines to extract per PDF.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if input_path.is_dir():
        output_dir = Path(args.output_dir) if args.output_dir else input_path / "_extracted_text"
        return _cli_extract_dir(input_path, output_dir, max_lines=max(1, args.max_lines))
    return _cli_extract_file(input_path, max_lines=max(1, args.max_lines))


if __name__ == "__main__":
    raise SystemExit(main())
