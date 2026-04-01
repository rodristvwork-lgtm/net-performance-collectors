import argparse
import socket
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class IperfScenario:
    name: str
    protocol: str
    direction: str


ALL_SCENARIOS = [
    IperfScenario(name="tcp_upload", protocol="tcp", direction="upload"),
    IperfScenario(name="tcp_download", protocol="tcp", direction="download"),
    IperfScenario(name="udp_upload", protocol="udp", direction="upload"),
    IperfScenario(name="udp_download", protocol="udp", direction="download"),
]


def get_local_ip() -> str:
    """Return the local source IP used to reach internet routes."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    finally:
        sock.close()


def build_result_file(
    protocol: str,
    direction: str,
    output_root: Path,
) -> Path:
    """Create a unique output file path for one test."""
    proto = protocol.upper()
    direction_tag = "DL" if direction == "download" else "UP"
    run_tag = f"{direction_tag}{proto}"

    target_dir = output_root / proto
    target_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%m%y")
    base_name = f"{run_tag}_iperf_{today}_"
    counter = 1
    while True:
        candidate = target_dir / f"{base_name}{counter}.txt"
        if not candidate.exists():
            return candidate
        counter += 1


def build_command(
    server_ip: str,
    duration: int,
    port: int,
    bind_ip: Optional[str],
    protocol: str,
    direction: str,
    bandwidth: str,
    connect_timeout_ms: int,
) -> List[str]:
    """Build iperf3 command from scenario parameters."""
    cmd = ["iperf3", "-c", server_ip, "-t", str(duration), "-p", str(port)]

    if bind_ip:
        cmd.extend(["-B", bind_ip])
    if protocol == "udp":
        cmd.extend(["-u", "-b", bandwidth])
    if direction == "download":
        cmd.append("-R")

    cmd.extend(["--connect-timeout", str(connect_timeout_ms)])
    cmd.append("--get-server-output")
    return cmd


def run_single_scenario(
    server_ip: str,
    duration: int,
    protocol: str,
    direction: str,
    start_port: int,
    end_port: int,
    udp_upload_bandwidth: str,
    udp_download_bandwidth: str,
    save: bool,
    output_root: Path,
    bind_ip: Optional[str],
    connect_timeout_ms: int,
    command_timeout_s: int,
) -> Tuple[bool, Optional[Path]]:
    """Try one scenario across a port range until success."""
    bandwidth = (
        udp_download_bandwidth
        if direction == "download"
        else udp_upload_bandwidth
    )
    for port in range(start_port, end_port + 1):
        cmd = build_command(
            server_ip=server_ip,
            duration=duration,
            port=port,
            bind_ip=bind_ip,
            protocol=protocol,
            direction=direction,
            bandwidth=bandwidth,
            connect_timeout_ms=connect_timeout_ms,
        )
        print(f"[{protocol.upper()} {direction.upper()}] trying port {port}")
        print("command:", " ".join(cmd))

        try:
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
                timeout=command_timeout_s,
            )
        except FileNotFoundError:
            print("Errore: 'iperf3' non trovato nel PATH.")
            return False, None
        except subprocess.TimeoutExpired:
            print(
                f"[{protocol.upper()} {direction.upper()}] timeout su porta "
                f"{port} dopo {command_timeout_s}s."
            )
            continue
        except OSError as exc:
            print(f"Errore OS durante esecuzione iperf3: {exc}")
            continue

        output = process.stdout or ""
        success = process.returncode == 0 and "iperf Done." in output
        if success:
            print(f"[{protocol.upper()} {direction.upper()}] test completato.")
            if save:
                file_path = build_result_file(protocol, direction, output_root)
                file_path.write_text(output, encoding="utf-8")
                print(f"Output salvato in: {file_path.resolve()}")
                return True, file_path
            return True, None

        print(
            f"[{protocol.upper()} {direction.upper()}] "
            f"fallito su porta {port} (rc={process.returncode})."
        )

    return False, None


def run_all_scenarios(
    server_ip: str,
    duration: int,
    start_port: int,
    end_port: int,
    udp_upload_bandwidth: str,
    udp_download_bandwidth: str,
    save: bool,
    output_root: Path,
    bind_ip: Optional[str],
    connect_timeout_ms: int,
    command_timeout_s: int,
) -> bool:
    """Run all TCP/UDP and upload/download tests."""
    results = {}
    saved_files: List[Path] = []
    for scenario in ALL_SCENARIOS:
        ok, saved_file = run_single_scenario(
            server_ip=server_ip,
            duration=duration,
            protocol=scenario.protocol,
            direction=scenario.direction,
            start_port=start_port,
            end_port=end_port,
            udp_upload_bandwidth=udp_upload_bandwidth,
            udp_download_bandwidth=udp_download_bandwidth,
            save=save,
            output_root=output_root,
            bind_ip=bind_ip,
            connect_timeout_ms=connect_timeout_ms,
            command_timeout_s=command_timeout_s,
        )
        results[scenario.name] = ok
        if saved_file is not None:
            saved_files.append(saved_file)

    print("\n=== RIEPILOGO TEST IPERF ===")
    for name, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"{name:12s}: {status}")
    if save:
        print(f"Directory risultati: {output_root.resolve()}")
        if saved_files:
            print("File salvati in questa esecuzione:")
            for path in saved_files:
                print(f"- {path.resolve()}")
        else:
            print("Nessun file salvato (nessun test completato con successo).")

    return all(results.values())


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Runner iperf3 per test TCP/UDP upload e download."
    )
    parser.add_argument("--server-ip", required=True, help="IP server iperf3")
    parser.add_argument(
        "--duration",
        type=int,
        default=20,
        help="Durata test (s)",
    )
    parser.add_argument(
        "--start-port",
        type=int,
        default=9212,
        help="Porta iniziale",
    )
    parser.add_argument(
        "--end-port",
        type=int,
        default=9240,
        help="Porta finale",
    )
    parser.add_argument(
        "--bandwidth",
        default="10M",
        help="Bandwidth UDP fallback (usata se non specifichi upload/download)",
    )
    parser.add_argument(
        "--udp-upload-bandwidth",
        default=None,
        help="Bandwidth UDP per upload (es. 10M, 100M, 1G)",
    )
    parser.add_argument(
        "--udp-download-bandwidth",
        default=None,
        help="Bandwidth UDP per download (es. 10M, 100M, 1G)",
    )
    parser.add_argument(
        "--bind-ip",
        default=None,
        help="IP locale da usare in bind (-B). Se omesso, auto-detect.",
    )
    parser.add_argument(
        "--connect-timeout-ms",
        type=int,
        default=3000,
        help="Timeout connessione client iperf3 in millisecondi",
    )
    parser.add_argument(
        "--command-timeout-s",
        type=int,
        default=None,
        help="Timeout hard per singolo comando iperf3 (secondi)",
    )
    parser.add_argument(
        "--scenario",
        choices=[s.name for s in ALL_SCENARIOS] + ["all"],
        default="all",
        help="Scenario da eseguire (default: all)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Salva output test in file sotto cartella results/",
    )
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Directory root dei risultati",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.start_port > args.end_port:
        parser.error("--start-port deve essere <= --end-port")

    bind_ip = args.bind_ip or get_local_ip()
    output_root = Path(args.output_dir)
    udp_upload_bandwidth = args.udp_upload_bandwidth or args.bandwidth
    udp_download_bandwidth = args.udp_download_bandwidth or args.bandwidth
    command_timeout_s = args.command_timeout_s or (args.duration + 15)
    if not args.save:
        print(
            "Salvataggio disabilitato: aggiungi --save per scrivere i risultati "
            "su file."
        )

    if args.scenario == "all":
        if args.save:
            print(f"I risultati verranno salvati in: {output_root.resolve()}")
        success = run_all_scenarios(
            server_ip=args.server_ip,
            duration=args.duration,
            start_port=args.start_port,
            end_port=args.end_port,
            udp_upload_bandwidth=udp_upload_bandwidth,
            udp_download_bandwidth=udp_download_bandwidth,
            save=args.save,
            output_root=output_root,
            bind_ip=bind_ip,
            connect_timeout_ms=args.connect_timeout_ms,
            command_timeout_s=command_timeout_s,
        )
    else:
        selected = next(s for s in ALL_SCENARIOS if s.name == args.scenario)
        if args.save:
            print(f"I risultati verranno salvati in: {output_root.resolve()}")
        success, saved_file = run_single_scenario(
            server_ip=args.server_ip,
            duration=args.duration,
            protocol=selected.protocol,
            direction=selected.direction,
            start_port=args.start_port,
            end_port=args.end_port,
            udp_upload_bandwidth=udp_upload_bandwidth,
            udp_download_bandwidth=udp_download_bandwidth,
            save=args.save,
            output_root=output_root,
            bind_ip=bind_ip,
            connect_timeout_ms=args.connect_timeout_ms,
            command_timeout_s=command_timeout_s,
        )
        if args.save:
            if saved_file is not None:
                print(f"File salvato: {saved_file.resolve()}")
            else:
                print("Nessun file salvato (test non completato con successo).")

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())