"""Small, dependency-free PEP 517 wheel backend for Product Manager OS.

The runtime is standard-library only, so its offline build must not depend on
an unpinned build package already being installed.  This backend deliberately
supports the one artifact this repository ships: a pure-Python wheel containing
``pmos`` and the manifest-bound runtime skill assets.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import tomllib
import zipfile
from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parent
PYPROJECT = ROOT / "pyproject.toml"
RUNTIME_MANIFEST = ROOT / "skills" / "runtime-manifest.json"
WHEEL_TAG = "py3-none-any"


def _project() -> Mapping[str, object]:
    with PYPROJECT.open("rb") as stream:
        return tomllib.load(stream)["project"]


def _normalized_name(name: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in name)


def _dist_info() -> str:
    project = _project()
    return "%s-%s.dist-info" % (
        _normalized_name(str(project["name"])), str(project["version"]),
    )


def _metadata() -> bytes:
    project = _project()
    authors = project.get("authors", [])
    author = authors[0].get("name", "") if isinstance(authors, list) and authors else ""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    headers = [
        "Metadata-Version: 2.1",
        "Name: %s" % project["name"],
        "Version: %s" % project["version"],
        "Summary: %s" % project["description"],
        "Requires-Python: %s" % project["requires-python"],
        "Description-Content-Type: text/markdown",
    ]
    if author:
        headers.append("Author: %s" % author)
    return ("\n".join(headers) + "\n\n" + readme + "\n").encode("utf-8")


def _wheel_metadata() -> bytes:
    return (
        "Wheel-Version: 1.0\n"
        "Generator: pmos-build-backend\n"
        "Root-Is-Purelib: true\n"
        "Tag: %s\n" % WHEEL_TAG
    ).encode("utf-8")


def _entry_points() -> bytes:
    return b"[console_scripts]\npmos = pmos.cli:main\n"


def _regular_bytes(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError("%s must be a regular file" % label)
    return path.read_bytes()


def _package_entries() -> dict[str, bytes]:
    entries: dict[str, bytes] = {}
    package_root = ROOT / "pmos"
    for path in sorted(package_root.rglob("*")):
        if "__pycache__" in path.parts or path.is_dir():
            continue
        if path.suffix != ".py" and path.name != "py.typed":
            continue
        relative = path.relative_to(package_root).as_posix()
        entries["pmos/" + relative] = _regular_bytes(path, "runtime package asset")

    raw_manifest = _regular_bytes(RUNTIME_MANIFEST, "runtime skill manifest")
    manifest = json.loads(raw_manifest.decode("utf-8"))
    trusted = manifest.get("skills")
    if not isinstance(trusted, dict) or not trusted:
        raise ValueError("runtime skill manifest has no skills")
    entries["pmos_runtime_assets/runtime-manifest.json"] = raw_manifest
    for skill_id, assets in sorted(trusted.items()):
        if not isinstance(skill_id, str) or not isinstance(assets, dict):
            raise ValueError("runtime skill manifest is invalid")
        for asset_name in sorted(assets):
            if not isinstance(asset_name, str):
                raise ValueError("runtime skill asset name is invalid")
            relative = Path(skill_id) / asset_name
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("runtime skill asset path is unsafe")
            source = ROOT / "skills" / "runtime" / relative
            archive_name = "pmos_runtime_assets/runtime/" + relative.as_posix()
            entries[archive_name] = _regular_bytes(source, "runtime skill asset")
    return entries


def _dist_info_entries() -> dict[str, bytes]:
    prefix = _dist_info() + "/"
    entries = {
        prefix + "METADATA": _metadata(),
        prefix + "WHEEL": _wheel_metadata(),
        prefix + "entry_points.txt": _entry_points(),
        prefix + "top_level.txt": b"pmos\npmos_runtime_assets\n",
        prefix + "licenses/LICENSE": _regular_bytes(ROOT / "LICENSE", "license"),
    }
    return entries


def _record(entries: Mapping[str, bytes]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    for name in sorted(entries):
        payload = entries[name]
        digest = base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).rstrip(b"=").decode("ascii")
        writer.writerow((name, "sha256=" + digest, len(payload)))
    writer.writerow((_dist_info() + "/RECORD", "", ""))
    return output.getvalue().encode("utf-8")


def _write_metadata(directory: Path) -> str:
    dist_info = _dist_info()
    target = directory / dist_info
    target.mkdir(parents=True, exist_ok=True)
    for name, payload in _dist_info_entries().items():
        relative = Path(name).relative_to(dist_info)
        output = target / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(payload)
    return dist_info


def get_requires_for_build_wheel(config_settings=None) -> list[str]:
    return []


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None) -> str:
    return _write_metadata(Path(metadata_directory))


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None) -> str:
    project = _project()
    filename = "%s-%s-%s.whl" % (
        _normalized_name(str(project["name"])), project["version"], WHEEL_TAG,
    )
    destination = Path(wheel_directory)
    destination.mkdir(parents=True, exist_ok=True)
    entries = _package_entries()
    entries.update(_dist_info_entries())
    entries[_dist_info() + "/RECORD"] = _record(entries)
    with zipfile.ZipFile(destination / filename, "w", compression=zipfile.ZIP_DEFLATED) as wheel:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o644 << 16
            wheel.writestr(info, entries[name])
    return filename
