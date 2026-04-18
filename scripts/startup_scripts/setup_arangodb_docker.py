from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

# Candidate install paths for Docker Desktop on Windows
_DOCKER_DESKTOP_PATHS = [
    r"C:\Program Files\Docker\Docker\Docker Desktop.exe",
    r"C:\Program Files (x86)\Docker\Docker\Docker Desktop.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Docker\Docker Desktop.exe"),
]


def _v3_root() -> Path:
    # parents[0] = startup_scripts/, parents[1] = scripts/, parents[2] = workspace root
    return Path(__file__).resolve().parents[2]


def _run(cmd: list[str], cwd: Path | None = None, dry_run: bool = False) -> None:
    location = f" (cwd={cwd})" if cwd else ""
    print(f"$ {' '.join(cmd)}{location}")
    if dry_run:
        return
    subprocess.run(cmd, check=True, cwd=str(cwd) if cwd else None)


def _docker_daemon_running() -> bool:
    """Return True if the Docker daemon is reachable."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


def _start_docker_desktop(dry_run: bool, wait_retries: int = 30, wait_delay: float = 3.0) -> None:
    """Launch Docker Desktop if the daemon is not already running."""
    if _docker_daemon_running():
        print("docker: daemon already running")
        return

    if dry_run:
        print("dry-run: would start Docker Desktop and wait for daemon")
        return

    exe = next((p for p in _DOCKER_DESKTOP_PATHS if Path(p).exists()), None)
    if exe is None:
        raise RuntimeError(
            "Docker Desktop not found. Install it from https://www.docker.com/products/docker-desktop/"
        )

    print(f"starting Docker Desktop: {exe}")
    subprocess.Popen([exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("waiting for Docker daemon to become ready...")
    for attempt in range(1, wait_retries + 1):
        time.sleep(wait_delay)
        if _docker_daemon_running():
            print(f"docker: daemon ready on attempt {attempt}/{wait_retries}")
            return
        print(f"  still waiting... ({attempt}/{wait_retries})")

    raise RuntimeError("Docker daemon did not become ready in time after launching Docker Desktop.")


def _ensure_env_file(docker_dir: Path, dry_run: bool) -> None:
    env_file = docker_dir / ".env"
    env_example = docker_dir / ".env.example"
    if env_file.exists():
        print(f"env ready: {env_file}")
        return
    if not env_example.exists():
        raise FileNotFoundError(f"missing .env.example: {env_example}")
    print(f"creating env from template: {env_file}")
    if not dry_run:
        env_file.write_text(env_example.read_text(encoding="utf-8"), encoding="utf-8")


def _read_arango_port(docker_dir: Path, default: int = 8529) -> int:
    env_file = docker_dir / ".env"
    if not env_file.exists():
        return default

    try:
        for raw in env_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() == "ARANGO_PORT":
                return int(value.strip())
    except Exception:
        pass

    return default


def _wait_for_arango(v3_root: Path, port: int, retries: int, delay: float, dry_run: bool) -> None:
    if dry_run:
        print("dry-run: skip arangodb health wait")
        return

    ops_path = v3_root / "Modules" / "arangodb" / "python-ops"
    if str(ops_path) not in sys.path:
        sys.path.insert(0, str(ops_path))

    from ops import arango_http_up

    for attempt in range(1, retries + 1):
        try:
            if arango_http_up(url=f"http://127.0.0.1:{port}/_api/version"):
                print(f"arangodb healthy on attempt {attempt}/{retries}")
                return
        except Exception:
            pass
        print(f"waiting for arangodb... attempt {attempt}/{retries}")
        time.sleep(delay)

    raise RuntimeError("arangodb did not become healthy in time")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Consolidated ArangoDB Docker setup demo for V3")
    parser.add_argument("--dry-run", action="store_true", help="Print commands only")
    parser.add_argument("--with-mcp", action="store_true", help="Also start mcp-arangodb profile")
    parser.add_argument("--retries", type=int, default=40, help="ArangoDB health check retries")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between retries (seconds)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    v3_root = _v3_root()
    docker_dir = v3_root / "Modules" / "docker"
    compose_file = docker_dir / "docker-compose.base.yml"

    if not docker_dir.exists():
        raise FileNotFoundError(f"missing docker module: {docker_dir}")
    if not compose_file.exists():
        raise FileNotFoundError(f"missing compose file: {compose_file}")

    print("V3 demo: setup arangodb via docker")
    print(f"v3_root={v3_root}")
    print("mode=dry-run" if args.dry_run else "mode=apply")

    _ensure_env_file(docker_dir, args.dry_run)
    arango_port = _read_arango_port(docker_dir)
    print(f"arango_host_port={arango_port}")
    _start_docker_desktop(args.dry_run)
    _run(["docker", "--version"], dry_run=args.dry_run)
    _run(["docker", "compose", "version"], dry_run=args.dry_run)

    up_cmd = ["docker", "compose"]
    if args.with_mcp:
        up_cmd.extend(["--profile", "mcp"])
    up_cmd.extend(["-f", str(compose_file), "up", "-d"])
    _run(up_cmd, cwd=docker_dir, dry_run=args.dry_run)

    _wait_for_arango(v3_root, port=arango_port, retries=args.retries, delay=args.delay, dry_run=args.dry_run)

    print("done: arangodb setup is ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
