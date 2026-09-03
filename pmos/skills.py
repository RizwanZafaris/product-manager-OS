"""Versioned, fail-closed contracts for runtime PMOS skills.

The runtime registry is deliberately small.  A skill is data (``SKILL.md``
and ``contract.json``), and the registry verifies its location, schema, and
content hashes before making it available to an executor.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional


class SkillContractError(ValueError):
    """Raised when a runtime skill is not safe or internally consistent."""


SkillValidationError = SkillContractError


_TOP_LEVEL = frozenset({
    "version", "id", "name", "description", "inputs", "outputs",
    "capabilities", "side_effects", "risk", "privacy", "allowed_hooks",
    "resume", "completion", "source_hash", "template_hashes",
})
_FIELD_KEYS = frozenset({"type", "required", "description", "items", "enum"})
_KNOWN_HOOKS = frozenset({
    "before_transition", "after_transition", "before_provider",
    "after_provider", "before_commit", "after_commit", "on_failure",
    "before_external", "after_external",
})
_MANIFEST_FORMAT = "pmos.skill-manifest/v1"
_MANIFEST_KEYS = frozenset({"format", "schema", "skills"})
_MANDATORY_ASSETS = frozenset({"contract.json", "SKILL.graph.yml", "SKILL.md"})
_GRAPH_KEYS = frozenset({"layer", "stage", "gate", "feeds", "method", "aliases"})


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_relative_bytes(root: Path, relative: str, label: str) -> bytes:
    """Read one regular asset through a pinned no-follow directory traversal."""
    parts = Path(relative).parts
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise SkillContractError("%s has an unsafe path" % label)
    descriptors: list[int] = []
    try:
        current = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) |
                          getattr(os, "O_NOFOLLOW", 0))
        descriptors.append(current)
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        for component in parts[:-1]:
            current = os.open(component, flags | getattr(os, "O_DIRECTORY", 0), dir_fd=current)
            descriptors.append(current)
        file_fd = os.open(parts[-1], flags, dir_fd=current)
        descriptors.append(file_fd)
        metadata = os.fstat(file_fd)
        if not stat.S_ISREG(metadata.st_mode):
            raise SkillContractError("%s must be a regular non-symlink file" % label)
        chunks = []
        while True:
            chunk = os.read(file_fd, 65536)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(file_fd)
        pathname = os.stat(parts[-1], dir_fd=current, follow_symlinks=False)
        if (metadata.st_dev != after.st_dev or metadata.st_ino != after.st_ino or
                metadata.st_size != after.st_size or not stat.S_ISREG(pathname.st_mode) or
                pathname.st_dev != metadata.st_dev or pathname.st_ino != metadata.st_ino):
            raise SkillContractError("%s changed while reading" % label)
        return b"".join(chunks)
    except SkillContractError:
        raise
    except OSError as exc:
        raise SkillContractError("cannot safely read %s" % label) from exc
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def _hash_value(value: Any) -> str:
    if not isinstance(value, str):
        raise SkillContractError("hash must be a hexadecimal sha256 string")
    value = value.strip().lower()
    if value.startswith("sha256:"):
        value = value[7:]
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise SkillContractError("hash must be a hexadecimal sha256 string")
    return value


def _safe_relative(root: Path, raw: Any, label: str) -> Path:
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        raise SkillContractError("%s must be a relative path" % label)
    relative = Path(raw)
    if any(part in ("", ".", "..") for part in relative.parts):
        raise SkillContractError("%s is not normalized" % label)
    candidate = (root / relative).resolve()
    cursor = root
    for component in relative.parts:
        cursor = cursor / component
        if cursor.is_symlink():
            raise SkillContractError("%s contains a symlink component" % label)
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise SkillContractError("%s escapes runtime root" % label) from exc
    return candidate


def _graph(path: Path | bytes) -> Mapping[str, Any]:
    """Parse the deliberately closed, scalar/list graph sidecar subset."""
    values: dict[str, Any] = {}
    try:
        lines = (path.decode("utf-8") if isinstance(path, bytes)
                 else path.read_text(encoding="utf-8")).splitlines()
    except (OSError, UnicodeError) as exc:
        raise SkillContractError("invalid skill graph") from exc
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise SkillContractError("invalid skill graph line")
        key, raw = line.split(":", 1)
        key, raw = key.strip(), raw.strip()
        if key in values or key not in _GRAPH_KEYS or not raw:
            raise SkillContractError("invalid or duplicate skill graph key")
        if raw.startswith("["):
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise SkillContractError("invalid graph list") from exc
            if not isinstance(parsed, list) or any(not isinstance(item, str) for item in parsed):
                raise SkillContractError("graph lists must contain strings")
            values[key] = parsed
        elif raw.isdigit():
            values[key] = int(raw)
        else:
            values[key] = raw.strip("\"'")
    if set(values) != _GRAPH_KEYS:
        raise SkillContractError("skill graph has missing or unknown keys")
    if values["layer"] != "skills" or not 1 <= values["gate"] <= 6:
        raise SkillContractError("skill graph has invalid layer or gate")
    return values


def _manifest_hash(value: Any) -> str:
    return _hash_value(value)


def _regular(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise SkillContractError("%s must be a regular non-symlink file" % label)


def _asset_paths(skill_dir: Path) -> set[str]:
    """Return all regular asset paths, rejecting symlink files/directories."""
    assets: set[str] = set()
    for current, dirs, names in os.walk(skill_dir, topdown=True, followlinks=False):
        if any(Path(current, name).is_symlink() for name in dirs):
            raise SkillContractError("skill contains a symlink directory")
        dirs[:] = sorted(dirs)
        # Empty/unpopulated directories are still untrusted tree entries.  A
        # manifest closes the complete shipped asset set, not just its files.
        if current != str(skill_dir) and not dirs and not names:
            raise SkillContractError("skill contains an empty asset directory")
        for name in sorted(names):
            path = Path(current, name)
            if path.is_symlink() or not path.is_file():
                raise SkillContractError("skill contains an unsafe asset")
            relative = path.relative_to(skill_dir).as_posix()
            if not relative or ".." in Path(relative).parts or "\\" in relative:
                raise SkillContractError("skill contains an unsafe asset path")
            assets.add(relative)
    return assets


def _fields(raw: Any, label: str) -> tuple["TypedField", ...]:
    if isinstance(raw, Mapping):
        entries = []
        for name, spec in raw.items():
            if not isinstance(name, str) or not name:
                raise SkillContractError("%s has an invalid field name" % label)
            if isinstance(spec, str):
                spec = {"type": spec}
            elif not isinstance(spec, Mapping):
                raise SkillContractError("%s.%s must be an object" % (label, name))
            entries.append({"name": name, **dict(spec)})
    elif isinstance(raw, list):
        entries = raw
    else:
        raise SkillContractError("%s must be an object or list" % label)
    result = []
    names = set()
    for item in entries:
        if not isinstance(item, Mapping):
            raise SkillContractError("%s entries must be objects" % label)
        unknown = set(item) - (_FIELD_KEYS | {"name"})
        if unknown or not isinstance(item.get("name"), str) or not item["name"]:
            raise SkillContractError("invalid or unknown %s field" % label)
        name = item["name"]
        if name in names:
            raise SkillContractError("duplicate %s field" % name)
        names.add(name)
        type_name = item.get("type")
        if not isinstance(type_name, str) or not type_name.strip():
            raise SkillContractError("%s.%s needs a type" % (label, name))
        required = item.get("required", False)
        if not isinstance(required, bool):
            raise SkillContractError("%s.%s.required must be boolean" % (label, name))
        enum = item.get("enum", ())
        if enum is None:
            enum = ()
        if not isinstance(enum, (list, tuple)):
            raise SkillContractError("%s.%s.enum must be a list" % (label, name))
        result.append(TypedField(name, type_name.strip(), required,
                                 str(item.get("description", "")), tuple(enum)))
    return tuple(result)


def _semantic(value: Any, label: str) -> Mapping[str, Any]:
    if isinstance(value, str):
        return {"status": value}
    if not isinstance(value, Mapping):
        raise SkillContractError("%s must be a string or object" % label)
    # Semantics are intentionally opaque but JSON-shaped; this preserves
    # forwards-compatible resume/completion details without executing them.
    try:
        json.dumps(value)
    except (TypeError, ValueError) as exc:
        raise SkillContractError("%s must be JSON data" % label) from exc
    return dict(value)


@dataclass(frozen=True)
class TypedField:
    name: str
    type: str
    required: bool = False
    description: str = ""
    enum: tuple[Any, ...] = ()


@dataclass(frozen=True)
class SkillContract:
    version: str
    id: str
    name: str
    description: str
    inputs: tuple[TypedField, ...]
    outputs: tuple[TypedField, ...]
    capabilities: frozenset[str]
    side_effects: frozenset[str]
    risk: str
    privacy: str
    allowed_hooks: frozenset[str]
    resume: Mapping[str, Any]
    completion: Mapping[str, Any]
    source_hash: str
    template_hashes: Mapping[str, str]
    path: Optional[Path] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any], *, path: Optional[Path] = None) -> "SkillContract":
        if not isinstance(data, Mapping):
            raise SkillContractError("contract must be a JSON object")
        unknown = set(data) - _TOP_LEVEL
        missing = _TOP_LEVEL - set(data)
        if unknown:
            raise SkillContractError("unknown contract field: %s" % sorted(unknown)[0])
        if missing:
            raise SkillContractError("missing contract field: %s" % sorted(missing)[0])
        strings = ("version", "id", "name", "description", "risk", "privacy")
        if any(not isinstance(data[key], str) or not data[key].strip() for key in strings):
            raise SkillContractError("contract scalar fields must be non-empty strings")
        def string_set(key: str) -> frozenset[str]:
            value = data[key]
            if not isinstance(value, (list, tuple, set)) or any(
                    not isinstance(item, str) or not item.strip() for item in value):
                raise SkillContractError("%s must be a list of strings" % key)
            return frozenset(item.strip() for item in value)
        hooks = string_set("allowed_hooks")
        if not hooks.issubset(_KNOWN_HOOKS):
            raise SkillContractError("unknown allowed hook")
        templates = data["template_hashes"]
        if not isinstance(templates, Mapping):
            raise SkillContractError("template_hashes must be an object")
        template_hashes = {}
        for raw_path, value in templates.items():
            if not isinstance(raw_path, str):
                raise SkillContractError("template hash path must be a string")
            # Path syntax is checked against the runtime root by the registry.
            template_hashes[raw_path] = _hash_value(value)
        return cls(
            version=data["version"].strip(), id=data["id"].strip(),
            name=data["name"].strip(), description=data["description"].strip(),
            inputs=_fields(data["inputs"], "inputs"),
            outputs=_fields(data["outputs"], "outputs"),
            capabilities=string_set("capabilities"), side_effects=string_set("side_effects"),
            risk=data["risk"].strip().lower(), privacy=data["privacy"].strip().lower(),
            allowed_hooks=hooks, resume=_semantic(data["resume"], "resume"),
            completion=_semantic(data["completion"], "completion"),
            source_hash=_hash_value(data["source_hash"]), template_hashes=template_hashes,
            path=path,
        )


class SkillRegistry:
    """Load only assets matching a separate trusted, closed manifest.

    The manifest is deliberately outside every mutable skill directory. A
    skill cannot change its own contract hashes, graph, or templates and make
    that change appear trusted; only the operator/release process can update
    the manifest.
    """

    def __init__(self, root: str | Path | None = None,
                 trusted_manifest: str | Path | None = None) -> None:
        if root is None:
            distribution_root = Path(__file__).resolve().parent.parent
            source_root = distribution_root / "skills" / "runtime"
            packaged_root = distribution_root / "pmos_runtime_assets" / "runtime"
            # A source checkout keeps the document and runtime skill tree in
            # ``skills/``. A built wheel maps that same canonical directory
            # into a data-only namespace package beside ``pmos``.
            root_input = source_root if source_root.is_dir() else packaged_root
        else:
            root_input = Path(root).expanduser()
        if root_input.is_symlink():
            raise SkillContractError("runtime root must not be a symlink")
        self.root = root_input.resolve()
        manifest_input = (Path(trusted_manifest).expanduser()
                          if trusted_manifest is not None
                          else self.root.parent / "runtime-manifest.json")
        if manifest_input.is_symlink():
            raise SkillContractError("trusted manifest must not be a symlink")
        self.trusted_manifest = manifest_input.resolve()
        try:
            self.trusted_manifest.relative_to(self.root)
        except ValueError:
            pass
        else:
            raise SkillContractError("trusted manifest must be outside the runtime root")
        self._contracts: dict[str, SkillContract] = {}

    @property
    def contracts(self) -> Mapping[str, SkillContract]:
        return dict(self._contracts)

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._contracts))

    def load(self) -> Mapping[str, SkillContract]:
        # Never leave a previously trusted snapshot active after a failed
        # reload; callers must observe the failure and explicitly recover.
        self._contracts = {}
        if not self.root.is_dir():
            raise SkillContractError("runtime root does not exist")
        try:
            manifest = json.loads(_read_relative_bytes(
                self.trusted_manifest.parent, self.trusted_manifest.name,
                "trusted skill manifest").decode("utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise SkillContractError("trusted skill manifest is missing or invalid") from exc
        if not isinstance(manifest, Mapping):
            raise SkillContractError("trusted skill manifest must be an object")
        unknown = set(manifest) - _MANIFEST_KEYS
        missing = _MANIFEST_KEYS - set(manifest)
        if unknown or missing or manifest.get("format") != _MANIFEST_FORMAT:
            raise SkillContractError("trusted skill manifest has invalid schema")
        if manifest.get("schema") != "pmos.skills.v1":
            raise SkillContractError("unsupported trusted skill manifest schema")
        trusted = manifest.get("skills")
        if not isinstance(trusted, Mapping) or not trusted:
            raise SkillContractError("trusted skill manifest has no skills")
        for skill_id, assets in trusted.items():
            if (not isinstance(skill_id, str) or not skill_id or
                    Path(skill_id).name != skill_id or "/" in skill_id or
                    "\\" in skill_id or skill_id in {".", ".."}):
                raise SkillContractError("trusted manifest has unsafe skill id")
            if not isinstance(assets, Mapping) or not _MANDATORY_ASSETS.issubset(set(assets)):
                raise SkillContractError("trusted manifest asset set is not closed")
            for asset_name, expected in assets.items():
                _manifest_hash(expected)
                asset_path = Path(asset_name)
                if (not asset_name or asset_path.is_absolute() or ".." in asset_path.parts or
                        "\\" in asset_name):
                    raise SkillContractError("trusted manifest has unsafe asset path")
        skill_dirs = []
        for child in self.root.iterdir():
            if child.is_symlink() or not child.is_dir() or child.name.startswith("."):
                raise SkillContractError("runtime root contains unknown or unsafe entry")
            skill_dirs.append(child.name)
        if set(skill_dirs) != set(trusted):
            raise SkillContractError("runtime skill set differs from trusted manifest")
        loaded: dict[str, SkillContract] = {}
        for skill_id in sorted(trusted):
            skill_dir = self.root / skill_id
            assets = trusted[skill_id]
            if skill_dir.is_symlink() or not skill_dir.is_dir():
                raise SkillContractError("runtime skill directory is unsafe")
            actual_assets = _asset_paths(skill_dir)
            if actual_assets != set(assets):
                raise SkillContractError("skill asset set differs from trusted manifest: %s" % skill_id)
            snapshots: dict[str, bytes] = {}
            for asset_name in sorted(assets):
                asset_path = _safe_relative(skill_dir, asset_name, "trusted asset path")
                _regular(asset_path, "%s/%s" % (skill_id, asset_name))
                snapshot = _read_relative_bytes(self.root, skill_id + "/" + asset_name,
                                                "%s/%s" % (skill_id, asset_name))
                snapshots[asset_name] = snapshot
                if hashlib.sha256(snapshot).hexdigest() != _manifest_hash(assets[asset_name]):
                    raise SkillContractError("trusted asset hash drift for %s/%s" % (skill_id, asset_name))
            _graph(snapshots["SKILL.graph.yml"])
            try:
                raw = json.loads(snapshots["contract.json"].decode("utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                raise SkillContractError("invalid contract JSON") from exc
            contract = SkillContract.from_mapping(raw, path=skill_dir / "contract.json")
            if contract.id != skill_dir.name:
                raise SkillContractError("contract id does not match directory")
            if contract.id in loaded:
                raise SkillContractError("duplicate skill id")
            if hashlib.sha256(snapshots["SKILL.md"]).hexdigest() != contract.source_hash:
                raise SkillContractError("source hash drift for %s" % contract.id)
            template_assets = set(assets) - set(_MANDATORY_ASSETS)
            if not template_assets or set(contract.template_hashes) != template_assets:
                raise SkillContractError("contract template set is not closed for %s" % contract.id)
            for raw_path, expected in contract.template_hashes.items():
                if raw_path not in snapshots:
                    raise SkillContractError("missing template for %s" % contract.id)
                actual = hashlib.sha256(snapshots[raw_path]).hexdigest()
                if actual != expected or actual != _manifest_hash(assets[raw_path]):
                    raise SkillContractError("template hash drift for %s" % contract.id)
            loaded[contract.id] = contract
        self._contracts = loaded
        return dict(loaded)

    discover = load

    def get(self, skill_id: str) -> SkillContract:
        if not self._contracts:
            self.load()
        try:
            return self._contracts[skill_id]
        except KeyError as exc:
            raise KeyError("unknown runtime skill: %s" % skill_id) from exc


__all__ = ["SkillContract", "SkillContractError", "SkillValidationError",
           "SkillRegistry", "TypedField"]
