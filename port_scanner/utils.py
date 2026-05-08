from __future__ import annotations

import ipaddress
import socket
from pathlib import Path


def validate_port_range(start_port: int, end_port: int) -> None:
    if not 1 <= start_port <= 65535:
        raise ValueError("Start port must be between 1 and 65535.")
    if not 1 <= end_port <= 65535:
        raise ValueError("End port must be between 1 and 65535.")
    if start_port > end_port:
        raise ValueError("Start port cannot be greater than end port.")


def validate_timeout(timeout: float) -> None:
    if timeout <= 0:
        raise ValueError("Timeout must be greater than 0 seconds.")


def validate_workers(workers: int) -> None:
    if not 1 <= workers <= 1000:
        raise ValueError("Workers must be between 1 and 1000.")


def resolve_target(target: str) -> tuple[str, str]:
    cleaned_target = target.strip()
    if not cleaned_target:
        raise ValueError("Target cannot be empty.")

    try:
        ipaddress.ip_address(cleaned_target)
        resolved_ip = cleaned_target
    except ValueError:
        try:
            resolved_ip = socket.gethostbyname(cleaned_target)
        except socket.gaierror as error:
            raise ValueError(f"Unable to resolve target '{cleaned_target}'.") from error

    return cleaned_target, resolved_ip


def ensure_output_directory(path_str: str | None) -> Path | None:
    if not path_str:
        return None

    output_path = Path(path_str).expanduser().resolve()
    if not output_path.suffix:
        output_path = output_path.with_suffix(".txt")
    if output_path.suffix.lower() not in {".txt", ".json"}:
        raise ValueError("Output file must use a .txt or .json extension.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def format_banner(raw_banner: bytes) -> str:
    cleaned = raw_banner.decode("utf-8", errors="replace").strip()
    cleaned = " ".join(cleaned.split())
    return cleaned if cleaned else "No banner captured"
