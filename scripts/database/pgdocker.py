"""Contenedor PostgreSQL desechable para C1: sin red, sin puertos, sin credenciales.

Solo biblioteca estándar. Cada instancia usa un nombre único y en la limpieza
elimina únicamente ese contenedor. No toca contenedores ajenos.
"""
from __future__ import annotations

import json
import subprocess
import time
import uuid
from dataclasses import dataclass
from typing import List, Optional, Sequence

DEFAULT_IMAGE = "postgres@sha256:d74eeac9a635390a49bc21bd49fccd973de707e2a53a76ac49b552b8712ec46f"
PG_UID = "999"
SOCKET_DIR = "/var/run/postgresql"
LABEL = "org.libox.c1=sql-overlay"
JSON_MARK = "LIBOXJSON:"


class DockerUnavailable(RuntimeError):
    pass


@dataclass
class PsqlResult:
    rc: int
    out: str
    err: str

    def failed_with(self, sqlstate: str, fragment: str = "") -> bool:
        """True si psql falló con ese SQLSTATE (VERBOSITY=verbose) y el fragmento."""
        marker = "ERROR:  " + sqlstate + ":"
        return self.rc != 0 and marker in self.err and fragment in self.err

    def error_line(self) -> str:
        for line in self.err.splitlines():
            if line.startswith("ERROR:"):
                return line.strip()
        return self.err.strip()[:300]


def run_command(argv: Sequence[str], data: Optional[bytes] = None, timeout: int = 180) -> subprocess.CompletedProcess:
    return subprocess.run(list(argv), input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=timeout, check=False)


def docker_server_version() -> str:
    res = run_command(["docker", "version", "--format", "{{.Server.Version}}"], timeout=30)
    if res.returncode != 0:
        raise DockerUnavailable(res.stderr.decode("utf-8", "replace").strip() or "docker no responde")
    return res.stdout.decode().strip()


def image_facts(image_id: str) -> dict:
    """Hechos de la imagen por su ID (tomado del contenedor en ejecución)."""
    res = run_command(["docker", "image", "inspect", image_id, "--format", "{{json .}}"], timeout=30)
    if res.returncode != 0:
        return {"id": image_id, "inspeccion": "no disponible"}
    data = json.loads(res.stdout.decode())
    return {"id": data.get("Id"), "repo_digests": sorted(data.get("RepoDigests") or []),
            "arquitectura": data.get("Architecture"), "so": data.get("Os")}


def build_run_command(name: str, image: str, allow_pull: bool = False) -> List[str]:
    """Orden docker run endurecida. Sin -p/--publish: ningún puerto expuesto."""
    return [
        "docker", "run", "--detach", "--rm",
        "--name", name,
        "--label", LABEL,
        "--network", "none",
        "--pull", "missing" if allow_pull else "never",
        "--user", PG_UID + ":" + PG_UID,
        "--read-only",
        "--tmpfs", "/var/lib/postgresql/data:rw,uid=999,gid=999,mode=0700,size=768m",
        "--tmpfs", SOCKET_DIR + ":rw,uid=999,gid=999,mode=2775",
        "--tmpfs", "/tmp:rw,uid=999,gid=999",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges:true",
        "--pids-limit", "512",
        "--env", "POSTGRES_HOST_AUTH_METHOD=trust",
        image,
    ]


class PgContainer:
    """Uso: with PgContainer(image, "escenario") as pg: pg.psql(...)."""

    def __init__(self, image: str = DEFAULT_IMAGE, tag: str = "c1", allow_pull: bool = False):
        self.image = image
        self.allow_pull = allow_pull
        self.name = "libox-c1-sql-" + tag + "-" + uuid.uuid4().hex[:10]
        self.started = False

    def __enter__(self) -> "PgContainer":
        try:
            self.start()
        except BaseException:
            # __exit__ no se llama si falla __enter__; limpiar el nombre propio
            # también cuando docker run agota el tiempo sin devolver el ID.
            self.remove()
            raise
        return self

    def __exit__(self, *exc) -> None:
        self.remove()

    def start(self, timeout: int = 120) -> None:
        self.started = True
        res = run_command(build_run_command(self.name, self.image, self.allow_pull), timeout=120)
        if res.returncode != 0:
            raise DockerUnavailable(res.stderr.decode("utf-8", "replace").strip())
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            logs = run_command(["docker", "logs", self.name], timeout=30)
            text = logs.stdout.decode("utf-8", "replace") + logs.stderr.decode("utf-8", "replace")
            if "PostgreSQL init process complete" in text:
                ready = run_command(["docker", "exec", self.name, "pg_isready", "-q", "-h", SOCKET_DIR], timeout=30)
                if ready.returncode == 0:
                    return
            time.sleep(1)
        raise DockerUnavailable("PostgreSQL no quedó listo en " + str(timeout) + " s")

    def remove(self) -> None:
        if self.started:
            run_command(["docker", "rm", "--force", self.name], timeout=60)
            self.started = False

    def image_id(self) -> str:
        res = run_command(["docker", "inspect", self.name, "--format", "{{.Image}}"], timeout=30)
        return res.stdout.decode().strip()

    def inspect_isolation(self) -> dict:
        res = run_command(["docker", "inspect", self.name, "--format",
                           "{{json .HostConfig.NetworkMode}}|{{json .NetworkSettings.Ports}}|{{json .HostConfig.PortBindings}}"],
                          timeout=30)
        mode, ports, bindings = res.stdout.decode().strip().split("|")
        return {"red": json.loads(mode), "puertos": json.loads(ports) or {},
                "enlaces_puerto": json.loads(bindings) or {}}

    def psql(self, sql: str, user: str = "postgres", db: str = "postgres", timeout: int = 300) -> PsqlResult:
        argv = ["docker", "exec", "--interactive", self.name, "psql", "-X", "-q", "-A", "-t",
                "-v", "ON_ERROR_STOP=1", "-v", "VERBOSITY=verbose",
                "-h", SOCKET_DIR, "-U", user, "-d", db]
        res = run_command(argv, data=sql.encode("utf-8"), timeout=timeout)
        return PsqlResult(res.returncode, res.stdout.decode("utf-8", "replace"),
                          res.stderr.decode("utf-8", "replace"))

    def psql_background(self, sql: str, user: str = "postgres", db: str = "postgres") -> subprocess.Popen:
        """Sesión psql en segundo plano (p. ej. para retener un bloqueo en una prueba).

        El llamador debe terminarla; al eliminar el contenedor también termina.
        """
        argv = ["docker", "exec", "--interactive", self.name, "psql", "-X", "-q", "-A", "-t",
                "-v", "ON_ERROR_STOP=1", "-h", SOCKET_DIR, "-U", user, "-d", db]
        proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert proc.stdin is not None
        proc.stdin.write(sql.encode("utf-8"))
        proc.stdin.close()
        return proc

    def json(self, query: str, user: str = "postgres", db: str = "postgres", prelude: str = ""):
        """Ejecuta query (que devuelve un valor json) y lo decodifica."""
        sql = prelude + "\nSELECT '" + JSON_MARK + "' || coalesce((" + query + ")::text, 'null');\n"
        res = self.psql(sql, user=user, db=db)
        if res.rc != 0:
            raise RuntimeError("consulta fallida: " + res.error_line())
        for line in res.out.splitlines():
            if line.startswith(JSON_MARK):
                return json.loads(line[len(JSON_MARK):])
        raise RuntimeError("sin salida JSON")
