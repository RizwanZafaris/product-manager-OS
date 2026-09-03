"""Bounded, deterministic model routing.

The router deliberately does not contain a model availability list.  A caller
supplies a catalog (or a discovery callable) and provider adapters.  Provider
credentials are identified by environment-variable *name* on ``ModelSpec``;
the value is read only at call time and is never put in a returned object.
"""

from __future__ import annotations

import builtins
import inspect
import math
import os
import re
import time
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, Callable, Iterable, Mapping, Optional, Sequence


class RouteStatus(str, Enum):
    ROUTED = "routed"
    BLOCKED = "blocked"
    ERROR = "error"


class ProviderError(Exception):
    """A safe provider failure category; messages are not retained by routes."""

    code = "provider_error"
    retryable = False


class ProviderRefusal(ProviderError):
    code = "refusal"


class ProviderRateLimit(ProviderError):
    code = "rate_limited"
    retryable = True


class ProviderTimeout(ProviderError):
    code = "timeout"
    retryable = True


class ProviderNetworkError(ProviderError):
    code = "network_error"
    retryable = True


class ProviderUnavailable(ProviderError):
    code = "provider_unavailable"
    retryable = True


class ProviderPolicyViolation(ProviderError):
    """A provider response violated a pre-authorized routing boundary."""

    code = "policy_violation"


class ModelUnavailable(ProviderError):
    code = "model_unavailable"
    retryable = True


# Friendly aliases for adapters that use the shorter conventional names.
RateLimitError = ProviderRateLimit
TimeoutError = ProviderTimeout
NetworkError = ProviderNetworkError


@dataclass(frozen=True)
class ModelSpec:
    """A discovered model and its caller-asserted policy metadata.

    ``certified`` is intentionally explicit.  Reachability, a low price, or a
    model name never implies certification.  ``privacy_classes`` and
    ``capabilities`` are supplied by discovery/configuration, not inferred.
    """

    provider: str
    model: str
    capabilities: frozenset[str] = frozenset()
    tools: frozenset[str] = frozenset()
    context_window: int = 0
    latency_ms: Optional[float] = None
    cost_per_1k_tokens: Optional[float] = None
    available: bool = True
    certified: bool = False
    certified_for: frozenset[str] = frozenset()
    free: bool = False
    privacy_classes: frozenset[str] = frozenset({"public"})
    priority: int = 0
    credential_env: Optional[str] = None

    def __post_init__(self) -> None:
        # Permit lists/sets from JSON discovery while preserving an immutable,
        # stable representation and avoiding mutable values in repr/results.
        for name in ("capabilities", "tools", "certified_for", "privacy_classes"):
            value = getattr(self, name)
            if isinstance(value, (str, bytes, bytearray, Mapping)):
                raise ValueError("%s must be a collection of strings" % name)
            try:
                items = tuple(value)
            except TypeError:
                raise ValueError("%s must be a collection of strings" % name) from None
            if any(not isinstance(item, str) or not item.strip() for item in items):
                raise ValueError("%s must contain only non-empty strings" % name)
            if (len(items) > 128 or any(
                    len(item) > 256 or any(ord(character) < 32 for character in item)
                    for item in items)):
                raise ValueError("%s exceeds the routing metadata bound" % name)
            object.__setattr__(self, name, frozenset(item.strip() for item in items))
        if (not isinstance(self.provider, str) or not self.provider.strip() or
                len(self.provider) > 128 or
                any(ord(character) < 32 for character in self.provider) or
                not isinstance(self.model, str) or not self.model.strip() or
                len(self.model) > 512 or
                any(ord(character) < 32 for character in self.model)):
            raise ValueError("provider and model must be non-empty strings")
        for name in ("available", "certified", "free"):
            if not isinstance(getattr(self, name), bool):
                raise ValueError("%s must be boolean" % name)
        if self.credential_env is not None and (
                not isinstance(self.credential_env, str) or
                not _ENV_NAME.fullmatch(self.credential_env)):
            raise ValueError("credential_env must be an environment-variable name")
        if (not isinstance(self.context_window, int) or
                isinstance(self.context_window, bool) or
                self.context_window < 0):
            raise ValueError("context_window must be non-negative")
        if (not isinstance(self.priority, int) or isinstance(self.priority, bool)
                or self.priority < 0):
            raise ValueError("priority must be non-negative")
        for name in ("latency_ms", "cost_per_1k_tokens"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, (int, float)) or
                                      isinstance(value, bool) or
                                      not math.isfinite(value) or value < 0):
                raise ValueError("%s must be a finite non-negative number" % name)


@dataclass(frozen=True)
class RoutingRequest:
    """The non-secret constraints for one model call."""

    prompt: str = ""
    task: str = ""
    risk: str = "low"
    privacy: str = "public"
    privacy_permission: Optional[str] = None
    capabilities: frozenset[str] = frozenset()
    required_tools: frozenset[str] = frozenset()
    context_tokens: int = 0
    max_latency_ms: Optional[float] = None
    budget_usd: Optional[float] = None
    estimated_tokens: Optional[int] = None
    max_output_tokens: int = 512
    max_attempts: Optional[int] = None

    def __post_init__(self) -> None:
        if not isinstance(self.prompt, str):
            raise ValueError("prompt must be a string")
        if not isinstance(self.task, str):
            raise ValueError("task must be a string")
        for name in ("risk", "privacy"):
            value = getattr(self, name)
            if (not isinstance(value, str) or not value.strip() or
                    len(value) > 128 or
                    any(ord(character) < 32 for character in value)):
                raise ValueError("%s must be a non-empty string" % name)
        if self.privacy_permission is not None and (
                not isinstance(self.privacy_permission, str) or
                not self.privacy_permission.strip() or
                len(self.privacy_permission) > 128 or
                any(ord(character) < 32 for character in self.privacy_permission)):
            raise ValueError("privacy_permission must be a non-empty string")
        if (len(self.task) > 256 or
                any(ord(character) < 32 for character in self.task)):
            raise ValueError("task exceeds the routing metadata bound")
        for name in ("capabilities", "required_tools"):
            value = getattr(self, name)
            if isinstance(value, (str, bytes, bytearray, Mapping)):
                raise ValueError("%s must be a collection of strings" % name)
            try:
                items = tuple(value)
            except TypeError:
                raise ValueError("%s must be a collection of strings" % name) from None
            if any(not isinstance(item, str) or not item.strip() for item in items):
                raise ValueError("%s must contain only non-empty strings" % name)
            if (len(items) > 128 or any(
                    len(item) > 256 or any(ord(character) < 32 for character in item)
                    for item in items)):
                raise ValueError("%s exceeds the routing metadata bound" % name)
            object.__setattr__(self, name, frozenset(item.strip() for item in items))
        if (not isinstance(self.context_tokens, int) or
                isinstance(self.context_tokens, bool) or
                self.context_tokens < 0):
            raise ValueError("context_tokens must be non-negative")
        if self.estimated_tokens is not None and (
                not isinstance(self.estimated_tokens, int) or
                isinstance(self.estimated_tokens, bool) or
                self.estimated_tokens < 0):
            raise ValueError("estimated_tokens must be non-negative")
        if (not isinstance(self.max_output_tokens, int) or
                isinstance(self.max_output_tokens, bool) or
                not 1 <= self.max_output_tokens <= 65536):
            raise ValueError("max_output_tokens must be between 1 and 65536")
        for name in ("max_latency_ms", "budget_usd"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, (int, float)) or
                                      isinstance(value, bool) or
                                      not math.isfinite(value) or value < 0):
                raise ValueError("%s must be a finite non-negative number" % name)
        if self.max_latency_ms == 0:
            raise ValueError("max_latency_ms must be positive when provided")
        if self.max_attempts is not None and (
                not isinstance(self.max_attempts, int) or
                isinstance(self.max_attempts, bool) or self.max_attempts < 1):
            raise ValueError("max_attempts must be a positive integer")

    @property
    def effective_privacy(self) -> str:
        """The stricter of data classification and caller permission.

        ``privacy_permission`` can raise a routing requirement (for example a
        tenant policy may demand restricted handling for internal data), but
        can never downgrade the classification on the data itself.
        """
        privacy = _norm(self.privacy)
        permission = _norm(self.privacy_permission) if self.privacy_permission else privacy
        if privacy not in _PRIVACY_RANK or permission not in _PRIVACY_RANK:
            return privacy if privacy not in _PRIVACY_RANK else permission
        return max((privacy, permission), key=_PRIVACY_RANK.__getitem__)


@dataclass(frozen=True)
class Attempt:
    provider: str
    model: str
    outcome: str
    reason: str


@dataclass(frozen=True)
class RouteDecision:
    """A safe, inspectable routing outcome.

    This object intentionally has no prompt, exception text, headers, request
    object, or credential.  ``provenance`` contains only allow-listed fields.
    """

    status: RouteStatus
    reason: str
    provider: Optional[str] = None
    model: Optional[str] = None
    output: Optional[str] = None
    provenance: Mapping[str, Any] = field(default_factory=dict)
    attempts: tuple[Attempt, ...] = ()
    error_code: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.status is RouteStatus.ROUTED

    @property
    def blocked(self) -> bool:
        return self.status is RouteStatus.BLOCKED


@dataclass(frozen=True)
class ProviderResponse:
    """Optional response shape provider adapters may return."""

    output: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    latency_ms: Optional[float] = None
    actual_model: Optional[str] = None


class EnvironmentSecrets:
    """Read credentials by environment-variable name without exposing values."""

    def __init__(self, environ: Optional[Mapping[str, str]] = None) -> None:
        self._environ = os.environ if environ is None else environ

    def get(self, name: Optional[str]) -> Optional[str]:
        if not name:
            return None
        return self._environ.get(name)

    def __repr__(self) -> str:
        return "EnvironmentSecrets(<environment-backed>)"


_PRIVACY_RANK = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}
_HIGH_RISK_TASKS = frozenset({"architecture", "security", "regulatory", "concurrency"})
_RISK_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
_ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
# A provider token can encode multiple Unicode bytes or a long whitespace run.
# This deliberately generous ceiling is a memory-safety backstop when a generic
# adapter cannot supply usage. Provider-specific adapters should still require
# authoritative token accounting.
_MAX_OUTPUT_BYTES_PER_TOKEN = 64


def _norm(value: Any) -> str:
    return str(value or "").strip().lower().replace(" ", "_")


def _safe_number(value: Any) -> Optional[float | int]:
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


class RiskTrustPolicy:
    """Explicit high-risk allowlist, independent of discovered model metadata.

    Discovery data is not a trust root: any catalog can claim ``certified``.
    Each entry therefore names an exact ``(provider, model)`` pair and one or
    more task/risk scopes. ``*`` allows all high-risk scopes for that exact
    model; wildcard providers or model names are intentionally unsupported.
    """

    def __init__(self, certifications: Mapping[tuple[str, str], Iterable[str]]) -> None:
        if not isinstance(certifications, Mapping):
            raise TypeError("risk certifications must be an explicit mapping")
        normalized: dict[tuple[str, str], frozenset[str]] = {}
        for key, values in certifications.items():
            if (not isinstance(key, tuple) or len(key) != 2 or
                    not all(isinstance(value, str) and value.strip() for value in key)):
                raise ValueError("risk policy keys must be exact (provider, model) pairs")
            provider, model = (_norm(key[0]), str(key[1]).strip())
            if provider == "*" or model == "*":
                raise ValueError("risk policy does not permit wildcard model identities")
            if isinstance(values, str):
                values = (values,)
            try:
                scopes = frozenset(_norm(value) for value in values)
            except TypeError:
                raise ValueError("risk policy scopes must be iterable") from None
            if not scopes or any(not scope for scope in scopes):
                raise ValueError("risk policy needs at least one non-empty scope")
            normalized[(provider, model)] = scopes
        self._certifications = normalized

    def permits(self, provider: str, model: str, task: str, risk: str) -> bool:
        scopes = self._certifications.get((_norm(provider), str(model).strip()), frozenset())
        return bool(scopes.intersection({_norm(task), _norm(risk), "*"}))

    def __repr__(self) -> str:
        return "RiskTrustPolicy(exact_models=%d)" % len(self._certifications)


class ModelRouter:
    """Route a request through an external catalog with bounded fallback."""

    HARD_MAX_ATTEMPTS = 8
    HARD_MAX_CATALOG_MODELS = 4096

    def __init__(
        self,
        catalog: Iterable[ModelSpec] | Mapping[str, Iterable[ModelSpec]] | Callable[[], Iterable[ModelSpec]],
        providers: Mapping[str, Any],
        *,
        secrets: Optional[EnvironmentSecrets] = None,
        max_attempts: int = 3,
        risk_trust_policy: Optional[RiskTrustPolicy] = None,
    ) -> None:
        if not 1 <= max_attempts <= self.HARD_MAX_ATTEMPTS:
            raise ValueError("max_attempts must be between 1 and 8")
        self.catalog = catalog
        self.providers = providers
        self.secrets = secrets or EnvironmentSecrets()
        self.max_attempts = max_attempts
        if risk_trust_policy is not None and not isinstance(risk_trust_policy, RiskTrustPolicy):
            raise TypeError("risk_trust_policy must be a RiskTrustPolicy")
        self.risk_trust_policy = risk_trust_policy

    def _discover(self, request: RoutingRequest) -> list[ModelSpec]:
        if callable(self.catalog):
            kwargs: dict[str, Any] = {}
            try:
                params = inspect.signature(self.catalog).parameters
                accepts_kwargs = any(
                    parameter.kind is inspect.Parameter.VAR_KEYWORD
                    for parameter in params.values())
                if accepts_kwargs or "request" in params:
                    kwargs["request"] = request
                if request.max_latency_ms is not None and (
                        accepts_kwargs or "timeout_seconds" in params):
                    kwargs["timeout_seconds"] = request.max_latency_ms / 1000.0
            except (TypeError, ValueError):
                # Opaque callables retain the original no-argument catalog
                # contract. Their duration is still checked by ``route``.
                kwargs = {}
            source = self.catalog(**kwargs)
        else:
            source = self.catalog
        values: list[ModelSpec] = []

        def extend_bounded(models: Iterable[ModelSpec]) -> None:
            if isinstance(models, (str, bytes, bytearray)):
                raise ProviderPolicyViolation()
            for model in models:
                if len(values) >= self.HARD_MAX_CATALOG_MODELS:
                    raise ProviderPolicyViolation()
                values.append(model)

        if isinstance(source, Mapping):
            for models in source.values():
                if isinstance(models, ModelSpec):
                    extend_bounded((models,))
                else:
                    extend_bounded(models)
            return values
        extend_bounded(source)
        return values

    @staticmethod
    def _reserved_cost(spec: ModelSpec, request: RoutingRequest) -> float:
        """Conservatively reserve a complete capped call at catalog pricing."""
        tokens = max(
            max(request.context_tokens, len(request.prompt.encode("utf-8"))) +
            request.max_output_tokens,
            request.estimated_tokens or 0,
            1,
        )
        return (spec.cost_per_1k_tokens or 0.0) * tokens / 1000

    def _eligible(self, spec: ModelSpec, request: RoutingRequest) -> tuple[bool, str]:
        task = _norm(request.task)
        risk = _norm(request.risk)
        declared_privacy = _norm(request.privacy)
        permission = (_norm(request.privacy_permission)
                      if request.privacy_permission is not None else declared_privacy)
        privacy = _norm(request.effective_privacy)
        if not spec.available:
            return False, "model unavailable"
        provider = self.providers.get(spec.provider)
        if provider is None:
            return False, "provider unavailable"
        if getattr(provider, "available", True) is False:
            return False, "provider unavailable"
        if not request.capabilities.issubset(spec.capabilities):
            return False, "required capabilities unavailable"
        if not request.required_tools.issubset(spec.tools):
            return False, "required tools unavailable"
        conservative_input = max(
            request.context_tokens, len(request.prompt.encode("utf-8")))
        if conservative_input + request.max_output_tokens > spec.context_window:
            return False, "context window too small"
        if request.max_latency_ms is not None and (
            spec.latency_ms is None or spec.latency_ms > request.max_latency_ms
        ):
            return False, "latency constraint unmet"
        if declared_privacy not in _PRIVACY_RANK or permission not in _PRIVACY_RANK:
            return False, "unknown privacy class"
        if risk not in _RISK_RANK:
            return False, "unknown risk class"
        supported_privacy = {_norm(item) for item in spec.privacy_classes}
        clearances = [_PRIVACY_RANK[item] for item in supported_privacy
                      if item in _PRIVACY_RANK]
        if not clearances or max(clearances) < _PRIVACY_RANK[privacy]:
            return False, "privacy permission rejected"
        sensitive = _RISK_RANK.get(risk, 99) >= _RISK_RANK["high"] or task in _HIGH_RISK_TASKS
        certified_scopes = {_norm(scope) for scope in spec.certified_for}
        certified_task = task in certified_scopes or risk in certified_scopes
        if sensitive:
            if not spec.certified and not certified_task:
                return False, "high-risk task requires certified model metadata"
            if self.risk_trust_policy is None or not self.risk_trust_policy.permits(
                    spec.provider, spec.model, task, risk):
                return False, "high-risk task requires explicit model trust policy"
        estimated_cost = self._reserved_cost(spec, request)
        if request.budget_usd is not None and spec.cost_per_1k_tokens is None:
            return False, "cost unknown for bounded-budget request"
        if request.budget_usd is not None and estimated_cost > request.budget_usd:
            return False, "budget exhausted"
        return True, "eligible"

    def route(self, request: RoutingRequest) -> RouteDecision:
        route_started = time.monotonic()
        try:
            specs = self._discover(request)
        except Exception:
            return RouteDecision(
                RouteStatus.ERROR,
                "model catalog discovery failed",
                error_code="catalog_discovery_failed",
            )
        if (request.max_latency_ms is not None and
                (time.monotonic() - route_started) * 1000 > request.max_latency_ms):
            return RouteDecision(
                RouteStatus.ERROR,
                "model catalog discovery exceeded the latency boundary",
                error_code="catalog_discovery_timeout",
            )
        eligible: list[ModelSpec] = []
        rejected: list[Attempt] = []
        for spec in specs:
            if not isinstance(spec, ModelSpec):
                continue
            ok, why = self._eligible(spec, request)
            if ok:
                eligible.append(spec)
            else:
                rejected.append(Attempt(spec.provider, spec.model, "skipped", why))
        eligible.sort(
            key=lambda s: (
                s.priority,
                s.cost_per_1k_tokens if s.cost_per_1k_tokens is not None else float("inf"),
                s.latency_ms if s.latency_ms is not None else float("inf"),
                s.provider,
                s.model,
            )
        )
        if not eligible:
            reason = "no eligible model: " + (
                "; ".join(sorted({attempt.reason for attempt in rejected}))
                if rejected
                else "catalog empty"
            )
            return RouteDecision(
                RouteStatus.BLOCKED, reason, attempts=tuple(rejected), error_code="no_eligible_model"
            )

        requested_attempts = request.max_attempts or self.max_attempts
        attempt_limit = min(max(1, requested_attempts), self.HARD_MAX_ATTEMPTS, len(eligible))
        attempts = list(rejected)
        selected: list[ModelSpec] = []
        reserved_total = 0.0
        for spec in eligible:
            if len(selected) >= attempt_limit:
                break
            reserve = self._reserved_cost(spec, request)
            if (request.budget_usd is not None and
                    reserved_total + reserve > request.budget_usd):
                attempts.append(Attempt(
                    spec.provider, spec.model, "skipped",
                    "fallback budget exhausted"))
                continue
            selected.append(spec)
            reserved_total += reserve
        if not selected:
            return RouteDecision(
                RouteStatus.BLOCKED,
                "no eligible model: fallback budget exhausted",
                attempts=tuple(attempts),
                error_code="no_eligible_model",
            )
        spent_total = 0.0
        for spec in selected:
            reserve = self._reserved_cost(spec, request)
            if (request.budget_usd is not None and
                    spent_total + reserve > request.budget_usd + 1e-12):
                attempts.append(Attempt(
                    spec.provider, spec.model, "skipped",
                    "fallback budget exhausted"))
                continue
            spend_recorded = False
            try:
                remaining_ms = None
                if request.max_latency_ms is not None:
                    remaining_ms = request.max_latency_ms - (
                        (time.monotonic() - route_started) * 1000)
                    if remaining_ms <= 0:
                        raise ProviderTimeout()
                call_started = time.monotonic()
                response = self._call(spec, request, remaining_ms=remaining_ms)
                call_latency_ms = (time.monotonic() - call_started) * 1000
                normalized = self._normalize_response(response)
                self._validate_usage(spec, request, normalized)
                reported_cost = normalized.get("cost_usd")
                usage_cost = self._usage_cost(spec, normalized)
                attempt_cost = max(
                    float(reported_cost) if reported_cost is not None else 0.0,
                    usage_cost if usage_cost is not None else 0.0,
                )
                if reported_cost is None and usage_cost is None:
                    # The provider may have charged before returning incomplete
                    # telemetry. Count the full reservation before considering
                    # a fallback, rather than presenting unknown spend as zero.
                    attempt_cost = reserve
                spent_total += attempt_cost
                spend_recorded = True
                if (spec.cost_per_1k_tokens is not None and
                        attempt_cost > reserve + 1e-12):
                    raise ProviderPolicyViolation()
                if (request.budget_usd is not None and
                        spent_total > request.budget_usd + 1e-12):
                    raise ProviderPolicyViolation()
                reported_latency = normalized.get("latency_ms")
                if request.max_latency_ms is not None and (
                        (time.monotonic() - route_started) * 1000 > request.max_latency_ms or
                        (reported_latency is not None and
                         reported_latency > remaining_ms)):
                    raise ProviderPolicyViolation()
                normalized["latency_ms"] = max(
                    call_latency_ms,
                    float(reported_latency) if reported_latency is not None else 0.0,
                )
                if (normalized.get("output_tokens") is not None and
                        normalized["output_tokens"] > request.max_output_tokens):
                    raise ProviderPolicyViolation()
                if (len(normalized["output"].encode("utf-8")) >
                        request.max_output_tokens * _MAX_OUTPUT_BYTES_PER_TOKEN):
                    raise ProviderPolicyViolation()
                actual_model = normalized.get("actual_model")
                # Model eligibility was evaluated for ``spec.model``.  A
                # provider-reported replacement has no independently trusted
                # privacy, cost, capability, or certification metadata here,
                # so accepting it would make every policy check refer to a
                # different model than the one that received the prompt.  All
                # reported substitution or missing identity therefore fails
                # closed for every request, not merely high-risk ones.
                if (not isinstance(actual_model, str) or
                        not actual_model.strip() or actual_model != spec.model):
                    raise ProviderPolicyViolation()
                attempts.append(Attempt(spec.provider, spec.model, "success", "provider response"))
                provenance = dict(self._provenance(spec, normalized))
                if request.budget_usd is not None or attempt_cost:
                    provenance["cumulative_cost_usd"] = spent_total
                return RouteDecision(
                    RouteStatus.ROUTED,
                    "selected eligible model",
                    provider=spec.provider,
                    model=actual_model,
                    output=normalized["output"],
                    provenance=provenance,
                    attempts=tuple(attempts),
                )
            except Exception as exc:  # provider boundaries must not break policy routing
                if request.budget_usd is not None and not spend_recorded:
                    spent_total += reserve
                code = self._error_code(exc)
                attempts.append(Attempt(spec.provider, spec.model, "failed", code))
        return RouteDecision(
            RouteStatus.ERROR,
            "fallback exhausted after bounded provider attempts",
            attempts=tuple(attempts),
            error_code="fallback_exhausted",
        )

    def _call(self, spec: ModelSpec, request: RoutingRequest, *,
              remaining_ms: Optional[float] = None) -> Any:
        provider = self.providers[spec.provider]
        if getattr(provider, "available", True) is False:
            raise ProviderUnavailable()
        method = getattr(provider, "complete", provider if callable(provider) else None)
        if method is None:
            raise ProviderUnavailable()
        secret = self.secrets.get(spec.credential_env)
        kwargs: dict[str, Any] = {}
        try:
            params = inspect.signature(method).parameters
            accepts_kwargs = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())
            supports_request = accepts_kwargs or "request" in params
            supports_timeout = accepts_kwargs or "timeout_seconds" in params
            if remaining_ms is not None and not (supports_request or supports_timeout):
                raise ProviderPolicyViolation()
            if accepts_kwargs or "request" in params:
                kwargs["request"] = (
                    replace(request, max_latency_ms=remaining_ms)
                    if remaining_ms is not None else request)
            if remaining_ms is not None and supports_timeout:
                kwargs["timeout_seconds"] = remaining_ms / 1000.0
            if accepts_kwargs or "api_key" in params:
                kwargs["api_key"] = secret
        except (TypeError, ValueError):
            if remaining_ms is not None:
                raise ProviderPolicyViolation() from None
            kwargs = {"request": request, "api_key": secret}
        return method(spec.model, request.prompt, **kwargs)

    @staticmethod
    def _normalize_response(response: Any) -> dict[str, Any]:
        if isinstance(response, str):
            return {"output": response}
        if isinstance(response, ProviderResponse):
            data = response.__dict__.copy()
        elif isinstance(response, Mapping):
            status = response.get("status_code", response.get("status"))
            if isinstance(status, int) and status >= 400:
                if status == 429:
                    raise ProviderRateLimit()
                if status in (408, 504):
                    raise ProviderTimeout()
                raise ProviderError()
            data = dict(response)
        else:
            data = {
                key: getattr(response, key)
                for key in ("output", "input_tokens", "output_tokens", "total_tokens",
                            "cost_usd", "latency_ms", "actual_model")
                if hasattr(response, key)
            }
        if data.get("refused") or data.get("refusal"):
            raise ProviderRefusal()
        if isinstance(data.get("error"), Mapping):
            error_type = _norm(data["error"].get("type"))
            if "refus" in error_type:
                raise ProviderRefusal()
            if "rate" in error_type or data["error"].get("code") == 429:
                raise ProviderRateLimit()
        if "output" not in data and isinstance(data.get("text"), str):
            data["output"] = data["text"]
        if "output" not in data and isinstance(data.get("choices"), Sequence) and data["choices"]:
            first = data["choices"][0]
            message = first.get("message", {}) if isinstance(first, Mapping) else {}
            if isinstance(message, Mapping) and isinstance(message.get("content"), str):
                data["output"] = message["content"]
        if ("output" not in data or not isinstance(data.get("output"), str)
                or not data["output"].strip()):
            raise ProviderError()
        for name in ("input_tokens", "output_tokens", "total_tokens"):
            value = data.get(name)
            if value is not None and (not isinstance(value, int) or
                                      isinstance(value, bool) or value < 0):
                raise ProviderPolicyViolation()
        for name in ("cost_usd", "latency_ms"):
            value = data.get(name)
            if value is not None and (not isinstance(value, (int, float)) or
                                      isinstance(value, bool) or
                                      not math.isfinite(value) or value < 0):
                raise ProviderPolicyViolation()
        if "actual_model" in data and data["actual_model"] is not None and (
                not isinstance(data["actual_model"], str) or
                not data["actual_model"].strip() or len(data["actual_model"]) > 512):
            raise ProviderPolicyViolation()
        return data

    @staticmethod
    def _validate_usage(spec: ModelSpec, request: RoutingRequest,
                        data: Mapping[str, Any]) -> None:
        input_tokens = data.get("input_tokens")
        output_tokens = data.get("output_tokens")
        total_tokens = data.get("total_tokens")
        if (input_tokens is not None and
                input_tokens + request.max_output_tokens > spec.context_window):
            raise ProviderPolicyViolation()
        if total_tokens is not None and total_tokens > spec.context_window:
            raise ProviderPolicyViolation()
        if (input_tokens is not None and output_tokens is not None and
                total_tokens is not None and
                total_tokens < input_tokens + output_tokens):
            raise ProviderPolicyViolation()
        if output_tokens == 0 and data.get("output", "").strip():
            raise ProviderPolicyViolation()

    @staticmethod
    def _usage_cost(spec: ModelSpec,
                    data: Mapping[str, Any]) -> Optional[float]:
        if spec.cost_per_1k_tokens is None:
            return None
        total = data.get("total_tokens")
        if total is None:
            input_tokens = data.get("input_tokens")
            output_tokens = data.get("output_tokens")
            if input_tokens is None or output_tokens is None:
                return None
            total = input_tokens + output_tokens
        return float(spec.cost_per_1k_tokens) * float(total) / 1000.0

    @staticmethod
    def _error_code(exc: Exception) -> str:
        if isinstance(exc, ProviderError):
            return exc.code
        status = getattr(exc, "status_code", getattr(exc, "status", None))
        if status == 429:
            return ProviderRateLimit.code
        if status in (408, 504):
            return ProviderTimeout.code
        if isinstance(exc, builtins.TimeoutError):
            return ProviderTimeout.code
        if isinstance(exc, ConnectionError):
            return ProviderNetworkError.code
        return ProviderNetworkError.code

    @staticmethod
    def _provenance(spec: ModelSpec, data: Mapping[str, Any]) -> Mapping[str, Any]:
        # Explicit allow-list prevents provider headers, prompt fragments, and
        # accidentally returned credentials from entering audit metadata.
        result: dict[str, Any] = {
            "provider": spec.provider,
            "model": (data.get("actual_model")
                      if isinstance(data.get("actual_model"), str) and
                      data.get("actual_model").strip() else spec.model),
            "requested_model": spec.model,
            "router_reason": "capability/risk/privacy/tools/context/latency/budget policy",
            "policy_reason": "eligible discovered model",
        }
        for source, target in (
            ("latency_ms", "latency_ms"),
            ("cost_usd", "cost_usd"),
            ("input_tokens", "input_tokens"),
            ("output_tokens", "output_tokens"),
            ("total_tokens", "total_tokens"),
        ):
            value = _safe_number(data.get(source))
            if value is not None:
                result[target] = value
        if "latency_ms" not in result and spec.latency_ms is not None:
            result["latency_ms"] = spec.latency_ms
        if spec.cost_per_1k_tokens is not None:
            result["cost_per_1k_tokens"] = spec.cost_per_1k_tokens
        return result


def route_model(
    request: RoutingRequest,
    catalog: Iterable[ModelSpec] | Mapping[str, Iterable[ModelSpec]] | Callable[[], Iterable[ModelSpec]],
    providers: Mapping[str, Any],
    **kwargs: Any,
) -> RouteDecision:
    """Convenience wrapper around :class:`ModelRouter`."""

    return ModelRouter(catalog, providers, **kwargs).route(request)


__all__ = [
    "Attempt",
    "EnvironmentSecrets",
    "ModelRouter",
    "ModelSpec",
    "ProviderError",
    "ProviderNetworkError",
    "ProviderRateLimit",
    "ProviderRefusal",
    "ProviderResponse",
    "ProviderPolicyViolation",
    "ProviderTimeout",
    "ProviderUnavailable",
    "RateLimitError",
    "TimeoutError",
    "NetworkError",
    "RouteDecision",
    "RouteStatus",
    "RoutingRequest",
    "RiskTrustPolicy",
    "route_model",
]
