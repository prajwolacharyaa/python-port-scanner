from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class PortResult:
    port: int
    state: str
    service_name: str
    banner: str
    response_time_ms: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ScanConfig:
    target: str
    start_port: int
    end_port: int
    timeout: float = 1.0
    workers: int = 100
    banner_bytes: int = 1024


@dataclass(slots=True)
class ScanSummary:
    target: str
    resolved_ip: str
    start_port: int
    end_port: int
    timeout: float
    workers: int
    started_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    finished_at: str | None = None
    duration_seconds: float = 0.0
    open_ports: list[PortResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "resolved_ip": self.resolved_ip,
            "start_port": self.start_port,
            "end_port": self.end_port,
            "timeout": self.timeout,
            "workers": self.workers,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "open_ports": [item.to_dict() for item in self.open_ports],
            "errors": self.errors,
        }
