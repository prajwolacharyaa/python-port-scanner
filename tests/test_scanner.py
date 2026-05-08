from __future__ import annotations

import json
import socket
import threading
import time
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from port_scanner.models import ScanConfig
from port_scanner.scanner import PortScanner
from port_scanner.utils import validate_port_range, validate_timeout, validate_workers
from port_scanner.writer import save_results


class BannerServer(threading.Thread):
    def __init__(self, banner: bytes = b"HELLO FROM TEST SERVICE\r\n") -> None:
        super().__init__(daemon=True)
        self.banner = banner
        self._ready = threading.Event()
        self._stop_event = threading.Event()
        self.port: int | None = None

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("127.0.0.1", 0))
            server.listen(5)
            server.settimeout(0.2)
            self.port = server.getsockname()[1]
            self._ready.set()

            while not self._stop_event.is_set():
                try:
                    client, _ = server.accept()
                except socket.timeout:
                    continue

                with client:
                    try:
                        client.sendall(self.banner)
                        time.sleep(0.05)
                    except OSError:
                        pass

    def start_and_wait(self) -> int:
        self.start()
        self._ready.wait(timeout=3)
        if self.port is None:
            raise RuntimeError("Test banner server did not start.")
        return self.port

    def stop(self) -> None:
        self._stop_event.set()


class PortScannerTests(unittest.TestCase):
    def test_scanner_detects_open_port_and_banner(self) -> None:
        server = BannerServer()
        open_port = server.start_and_wait()
        closed_port = open_port + 1

        try:
            config = ScanConfig(
                target="127.0.0.1",
                start_port=open_port,
                end_port=closed_port,
                timeout=0.5,
                workers=10,
            )
            summary = PortScanner(config).scan()
        finally:
            server.stop()

        self.assertEqual(summary.resolved_ip, "127.0.0.1")
        self.assertEqual(len(summary.open_ports), 1)
        result = summary.open_ports[0]
        self.assertEqual(result.port, open_port)
        self.assertEqual(result.state, "open")
        self.assertIn("HELLO FROM TEST SERVICE", result.banner)

    def test_writer_saves_json_report(self) -> None:
        server = BannerServer()
        open_port = server.start_and_wait()

        try:
            summary = PortScanner(
                ScanConfig(
                    target="127.0.0.1",
                    start_port=open_port,
                    end_port=open_port,
                    timeout=0.5,
                    workers=5,
                )
            ).scan()
        finally:
            server.stop()

        with TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "report.json"
            save_results(summary, output_file)
            payload = json.loads(output_file.read_text(encoding="utf-8"))

        self.assertEqual(payload["target"], "127.0.0.1")
        self.assertEqual(payload["open_ports"][0]["port"], open_port)

    def test_validation_guards(self) -> None:
        with self.assertRaises(ValueError):
            validate_port_range(100, 10)
        with self.assertRaises(ValueError):
            validate_timeout(0)
        with self.assertRaises(ValueError):
            validate_workers(0)


if __name__ == "__main__":
    unittest.main()
