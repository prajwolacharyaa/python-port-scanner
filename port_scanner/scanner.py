from __future__ import annotations

import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from port_scanner.models import PortResult, ScanConfig, ScanSummary
from port_scanner.utils import format_banner, resolve_target, validate_port_range, validate_timeout, validate_workers


class PortScanner:
    """Scan a target for open TCP ports and attempt banner detection."""

    def __init__(self, config: ScanConfig) -> None:
        validate_port_range(config.start_port, config.end_port)
        validate_timeout(config.timeout)
        validate_workers(config.workers)
        self.config = config
        self.target, self.resolved_ip = resolve_target(config.target)

    def scan(self) -> ScanSummary:
        summary = ScanSummary(
            target=self.target,
            resolved_ip=self.resolved_ip,
            start_port=self.config.start_port,
            end_port=self.config.end_port,
            timeout=self.config.timeout,
            workers=self.config.workers,
        )

        started = time.perf_counter()
        ports = range(self.config.start_port, self.config.end_port + 1)

        with ThreadPoolExecutor(max_workers=self.config.workers) as executor:
            future_map = {executor.submit(self._scan_single_port, port): port for port in ports}

            for future in as_completed(future_map):
                port = future_map[future]
                try:
                    result = future.result()
                except Exception as error:  # pragma: no cover - defensive branch
                    summary.errors.append(f"Unexpected error while scanning port {port}: {error}")
                    continue

                if result:
                    summary.open_ports.append(result)

        summary.open_ports.sort(key=lambda item: item.port)
        summary.duration_seconds = round(time.perf_counter() - started, 3)
        summary.finished_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        return summary

    def _scan_single_port(self, port: int) -> PortResult | None:
        socket_start = time.perf_counter()

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.config.timeout)
                connection_result = sock.connect_ex((self.resolved_ip, port))
                response_time_ms = round((time.perf_counter() - socket_start) * 1000, 2)

                if connection_result != 0:
                    return None

                service_name = self._safe_service_name(port)
                banner = self._grab_banner(sock, port)

                return PortResult(
                    port=port,
                    state="open",
                    service_name=service_name,
                    banner=banner,
                    response_time_ms=response_time_ms,
                )
        except (socket.timeout, ConnectionError, OSError):
            return None

    def _grab_banner(self, sock: socket.socket, port: int) -> str:
        try:
            probe = self._build_probe(port)
            if probe:
                sock.sendall(probe)

            banner = sock.recv(self.config.banner_bytes)
            return format_banner(banner)
        except (socket.timeout, ConnectionError, OSError):
            return "Banner unavailable"

    @staticmethod
    def _build_probe(port: int) -> bytes:
        if port in {80, 8080, 8000, 8888}:
            return b"HEAD / HTTP/1.0\r\nHost: target\r\n\r\n"
        if port in {21, 25, 110, 143}:
            return b"\r\n"
        return b""

    @staticmethod
    def _safe_service_name(port: int) -> str:
        try:
            return socket.getservbyport(port, "tcp")
        except OSError:
            return "unknown"
