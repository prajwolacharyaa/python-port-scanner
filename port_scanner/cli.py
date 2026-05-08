from __future__ import annotations

import argparse
import sys
from pathlib import Path

from port_scanner import __version__
from port_scanner.models import ScanConfig
from port_scanner.scanner import PortScanner
from port_scanner.utils import ensure_output_directory
from port_scanner.writer import save_results

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="port-scanner",
        description="Professional beginner-friendly TCP port scanner with banner grabbing.",
    )
    parser.add_argument("target", help="Target IP address or hostname to scan.")
    parser.add_argument("-s", "--start-port", type=int, default=1, help="Start of port range.")
    parser.add_argument("-e", "--end-port", type=int, default=1024, help="End of port range.")
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=1.0,
        help="Socket timeout in seconds for each connection attempt.",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=100,
        help="Maximum number of worker threads.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output file path. Supported formats: .txt and .json",
    )
    parser.add_argument(
        "--banner-bytes",
        type=int,
        default=1024,
        help="Maximum number of bytes to capture during banner grabbing.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def print_banner() -> None:
    lines = [
        f"{CYAN}{BOLD}============================================================{RESET}",
        f"{CYAN}{BOLD}  Professional Port Scanner{RESET}",
        f"{CYAN}  Reconnaissance and service detection for authorized labs{RESET}",
        f"{CYAN}{BOLD}============================================================{RESET}",
    ]
    print("\n".join(lines))


def print_summary(summary, output_path: Path | None) -> None:
    print(f"\n{BOLD}Scan Summary{RESET}")
    print(f"Target       : {summary.target} ({summary.resolved_ip})")
    print(f"Port Range   : {summary.start_port}-{summary.end_port}")
    print(f"Open Ports   : {len(summary.open_ports)}")
    print(f"Duration     : {summary.duration_seconds} seconds")

    if summary.open_ports:
        print(f"\n{BOLD}Discovered Services{RESET}")
        header = f"{'PORT':<8}{'STATE':<10}{'SERVICE':<18}{'RESPONSE':<12}BANNER"
        print(header)
        print("-" * len(header))
        for result in summary.open_ports:
            banner = result.banner if len(result.banner) <= 60 else f"{result.banner[:57]}..."
            print(
                f"{GREEN}{result.port:<8}{RESET}"
                f"{result.state:<10}"
                f"{result.service_name:<18}"
                f"{str(result.response_time_ms) + ' ms':<12}"
                f"{banner}"
            )
    else:
        print(f"{YELLOW}No open ports found in the selected range.{RESET}")

    if summary.errors:
        print(f"\n{RED}Warnings{RESET}")
        for item in summary.errors:
            print(f"- {item}")

    if output_path:
        print(f"\n{GREEN}Results saved to:{RESET} {output_path}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = ScanConfig(
            target=args.target,
            start_port=args.start_port,
            end_port=args.end_port,
            timeout=args.timeout,
            workers=args.workers,
            banner_bytes=args.banner_bytes,
        )
        scanner = PortScanner(config)
        print_banner()
        summary = scanner.scan()

        output_path = ensure_output_directory(args.output)
        if output_path:
            save_results(summary, output_path)

        print_summary(summary, output_path)
        return 0
    except KeyboardInterrupt:
        print(f"\n{RED}Scan interrupted by user.{RESET}")
        return 130
    except ValueError as error:
        print(f"\n{RED}Input error:{RESET} {error}", file=sys.stderr)
        return 1
    except Exception as error:  # pragma: no cover - defensive branch
        print(f"\n{RED}Unexpected error:{RESET} {error}", file=sys.stderr)
        return 1
