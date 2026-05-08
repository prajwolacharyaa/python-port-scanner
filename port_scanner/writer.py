from __future__ import annotations

import json
from pathlib import Path

from port_scanner.models import ScanSummary


def save_results(summary: ScanSummary, output_path: Path) -> Path:
    suffix = output_path.suffix.lower()

    if suffix == ".json":
        output_path.write_text(json.dumps(summary.to_dict(), indent=2), encoding="utf-8")
    else:
        output_path.write_text(_build_text_report(summary), encoding="utf-8")

    return output_path


def _build_text_report(summary: ScanSummary) -> str:
    lines = [
        "Port Scanner Report",
        "=" * 60,
        f"Target: {summary.target}",
        f"Resolved IP: {summary.resolved_ip}",
        f"Port Range: {summary.start_port}-{summary.end_port}",
        f"Timeout: {summary.timeout} seconds",
        f"Workers: {summary.workers}",
        f"Started At: {summary.started_at}",
        f"Finished At: {summary.finished_at}",
        f"Duration: {summary.duration_seconds} seconds",
        "",
        "Open Ports",
        "-" * 60,
    ]

    if not summary.open_ports:
        lines.append("No open ports found in the selected range.")
    else:
        for result in summary.open_ports:
            lines.extend(
                [
                    f"Port: {result.port}",
                    f"State: {result.state}",
                    f"Service: {result.service_name}",
                    f"Banner: {result.banner}",
                    f"Response Time: {result.response_time_ms} ms",
                    "-" * 60,
                ]
            )

    if summary.errors:
        lines.extend(["", "Errors", "-" * 60, *summary.errors])

    return "\n".join(lines).rstrip() + "\n"
