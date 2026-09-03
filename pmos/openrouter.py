"""Small standard-library OpenRouter adapter.

The adapter intentionally performs no live discovery at import time.  It
reads the configured environment variable only while making a request and
never retains or includes the credential or prompt in an exception/repr.
"""

from __future__ import annotations

import builtins
import ipaddress
import json
import math
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional

from .routing import (
    ModelSpec,
    ProviderError,
    ProviderNetworkError,
    ProviderRateLimit,
    ProviderRefusal,
    ProviderResponse,
    ProviderTimeout,
)


class OpenRouterError(ProviderError):
    code = "openrouter_error"


class OpenRouterAuthError(OpenRouterError):
    code = "auth_error"


class OpenRouterAuthMissing(OpenRouterAuthError):
    code = "auth_missing"


class OpenRouterMalformedResponse(OpenRouterError):
    code = "malformed_response"


class OpenRouterResponseTooLarge(OpenRouterError):
    code = "response_too_large"


class OpenRouterRedirectError(OpenRouterError):
    code = "redirect_rejected"


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Never forward an authorization header through an HTTP redirect."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_SAFE_OPENER = urllib.request.build_opener(_NoRedirectHandler()).open
_OFFICIAL_HOST = "openrouter.ai"
_ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _is_loopback(host: str) -> bool:
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _normalized_host(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("trusted hosts must be non-empty host names")
    candidate = value.strip().lower().rstrip(".")
    try:
        return ipaddress.ip_address(candidate).compressed
    except ValueError:
        pass
    if any(character in candidate for character in "/:@?#%"):
        raise ValueError("trusted hosts must not contain URL syntax")
    try:
        candidate = candidate.encode("idna").decode("ascii")
    except UnicodeError:
        raise ValueError("trusted host is invalid") from None
    if (not candidate or len(candidate) > 253 or
            any(not label or len(label) > 63 or label.startswith("-") or
                label.endswith("-") or
                not re.fullmatch(r"[a-z0-9-]+", label)
                for label in candidate.split("."))):
        raise ValueError("trusted host is invalid")
    return candidate


def _origin(value: str) -> Optional[tuple[str, str, int]]:
    """Normalize an absolute URL origin; return None for malformed values."""
    try:
        parsed = urllib.parse.urlsplit(value)
        host = _normalized_host(parsed.hostname or "")
        port = parsed.port
    except (TypeError, ValueError):
        return None
    scheme = parsed.scheme.lower()
    if port is None:
        port = 443 if scheme == "https" else 80 if scheme == "http" else -1
    return scheme, host, port


@dataclass(frozen=True)
class OpenRouterResponse(ProviderResponse):
    """Provider response with the actual model selected by OpenRouter."""

    @property
    def model(self) -> Optional[str]:
        return self.actual_model


@dataclass(frozen=True)
class OpenRouterConfig:
    api_key_env: str = "OPENROUTER_API_KEY"
    base_url: str = "https://openrouter.ai"
    timeout_seconds: float = 20.0
    max_response_bytes: int = 2 * 1024 * 1024
    max_request_bytes: int = 512 * 1024
    default_max_output_tokens: int = 1024
    attribution_headers: Mapping[str, str] = None
    trusted_hosts: frozenset[str] = frozenset()
    allow_insecure_test_transport: bool = False

    def __post_init__(self) -> None:
        if (not isinstance(self.api_key_env, str) or
                not _ENV_NAME.fullmatch(self.api_key_env)):
            raise ValueError("api_key_env must be an environment-variable name")
        if (not isinstance(self.timeout_seconds, (int, float)) or
                isinstance(self.timeout_seconds, bool) or
                not 0.1 <= float(self.timeout_seconds) <= 60):
            raise ValueError("timeout_seconds must be between 0.1 and 60")
        if (not isinstance(self.max_response_bytes, int) or
                isinstance(self.max_response_bytes, bool) or
                not 1024 <= self.max_response_bytes <= 8 * 1024 * 1024):
            raise ValueError("max_response_bytes is outside the safe bound")
        if (not isinstance(self.max_request_bytes, int) or
                isinstance(self.max_request_bytes, bool) or
                not 1024 <= self.max_request_bytes <= 2 * 1024 * 1024):
            raise ValueError("max_request_bytes is outside the safe bound")
        if (not isinstance(self.default_max_output_tokens, int) or
                isinstance(self.default_max_output_tokens, bool) or
                not 1 <= self.default_max_output_tokens <= 65536):
            raise ValueError("default_max_output_tokens must be between 1 and 65536")
        headers = self.attribution_headers or {}
        if not isinstance(headers, Mapping):
            raise ValueError("attribution_headers must be a mapping")
        cleaned = {}
        for name, value in headers.items():
            if name not in ("HTTP-Referer", "X-Title"):
                raise ValueError("only OpenRouter attribution headers are supported")
            if (not isinstance(value, str) or not value or len(value) > 512 or
                    any(ord(character) < 32 for character in value)):
                raise ValueError("attribution header values must be short strings")
            cleaned[str(name)] = value
        object.__setattr__(self, "attribution_headers", cleaned)
        if not isinstance(self.allow_insecure_test_transport, bool):
            raise ValueError("allow_insecure_test_transport must be boolean")
        raw_hosts = self.trusted_hosts
        if isinstance(raw_hosts, str):
            raise ValueError("trusted_hosts must be a collection, not a string")
        try:
            trusted_hosts = frozenset(_normalized_host(host) for host in raw_hosts)
        except TypeError:
            raise ValueError("trusted_hosts must be a collection") from None
        object.__setattr__(self, "trusted_hosts", trusted_hosts)

        try:
            parsed = urllib.parse.urlsplit(self.base_url)
            port = parsed.port
        except (TypeError, ValueError):
            raise ValueError("base_url must be a valid origin") from None
        if (not isinstance(self.base_url, str) or not parsed.hostname or
                parsed.username is not None or parsed.password is not None or
                parsed.query or parsed.fragment or parsed.path not in ("", "/")):
            raise ValueError("base_url must be an origin without credentials, path, query, or fragment")
        host = _normalized_host(parsed.hostname)
        scheme = parsed.scheme.lower()
        official = host == _OFFICIAL_HOST and port in (None, 443)
        if not official and host not in trusted_hosts:
            raise ValueError("non-official base_url host needs an explicit trusted_hosts entry")
        if scheme != "https":
            if not (scheme == "http" and self.allow_insecure_test_transport and
                    host in trusted_hosts and _is_loopback(host)):
                raise ValueError("base_url must use HTTPS; insecure test transport is loopback-only")
        if official and scheme != "https":
            raise ValueError("the official OpenRouter origin must use HTTPS")
        display_host = "[%s]" % host if ":" in host else host
        default_port = (scheme == "https" and port in (None, 443)) or \
                       (scheme == "http" and port in (None, 80))
        origin = "%s://%s%s" % (
            scheme, display_host, "" if default_port else ":%d" % port)
        object.__setattr__(self, "base_url", origin)


def _number(value: Any) -> Optional[float]:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


class OpenRouterProvider:
    """OpenRouter implementation compatible with ``ModelRouter``."""

    provider = "openrouter"

    def __init__(self, config: Optional[OpenRouterConfig] = None, *,
                 api_key_env: Optional[str] = None,
                 base_url: Optional[str] = None,
                 timeout_seconds: Optional[float] = None,
                 max_response_bytes: Optional[int] = None,
                 max_request_bytes: Optional[int] = None,
                 default_max_output_tokens: Optional[int] = None,
                 attribution_headers: Optional[Mapping[str, str]] = None,
                 trusted_hosts: Optional[frozenset[str]] = None,
                 allow_insecure_test_transport: Optional[bool] = None,
                 environ: Optional[Mapping[str, str]] = None,
                 urlopen: Optional[Callable[..., Any]] = None) -> None:
        if config is not None and any(value is not None for value in (
                api_key_env, base_url, timeout_seconds, max_response_bytes,
                max_request_bytes, default_max_output_tokens,
                attribution_headers, trusted_hosts,
                allow_insecure_test_transport)):
            raise ValueError("use config or direct options, not both")
        self.config = config or OpenRouterConfig(
            api_key_env=("OPENROUTER_API_KEY" if api_key_env is None else api_key_env),
            base_url=("https://openrouter.ai" if base_url is None else base_url),
            timeout_seconds=20.0 if timeout_seconds is None else timeout_seconds,
            max_response_bytes=(2 * 1024 * 1024 if max_response_bytes is None
                                else max_response_bytes),
            max_request_bytes=(512 * 1024 if max_request_bytes is None
                                else max_request_bytes),
            default_max_output_tokens=(1024 if default_max_output_tokens is None
                                       else default_max_output_tokens),
            attribution_headers=attribution_headers,
            trusted_hosts=frozenset() if trusted_hosts is None else trusted_hosts,
            allow_insecure_test_transport=(False if allow_insecure_test_transport is None
                                           else allow_insecure_test_transport),
        )
        parsed = urllib.parse.urlsplit(self.config.base_url)
        self._insecure_test_transport = parsed.scheme == "http"
        if self._insecure_test_transport and urlopen is None:
            raise ValueError("insecure test transport requires an injected transport")
        # This is a live mapping, not a copied secret.  Values are read only
        # inside _credential and never assigned to an instance attribute.
        self._environ = environ
        self._urlopen = urlopen or _SAFE_OPENER
        self.available = True

    def __repr__(self) -> str:
        return "OpenRouterProvider(api_key_env=%r, base_url=%r)" % (
            self.config.api_key_env, self.config.base_url)

    def _credential(self) -> str:
        source = self._environ
        if source is None:
            import os
            source = os.environ
        value = source.get(self.config.api_key_env)
        if not isinstance(value, str) or not value.strip() or any(
                character in value for character in "\r\n"):
            raise OpenRouterAuthMissing()
        return value

    def _headers(self, credential: Optional[str]) -> dict[str, str]:
        # The resulting header exists only on the short-lived request object.
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            **dict(self.config.attribution_headers),
        }
        if credential is not None:
            headers["Authorization"] = "Bearer " + credential
        return headers

    def _json_request(self, path: str, *, method: str = "GET",
                      payload: Optional[Mapping[str, Any]] = None,
                      timeout_seconds: Optional[float] = None,
                      max_response_bytes: Optional[int] = None,
                      api_key: Optional[str] = None) -> Mapping[str, Any]:
        if path not in ("/api/v1/models", "/api/v1/chat/completions"):
            raise OpenRouterError()
        # Plain HTTP is accepted only for an explicitly injected loopback test
        # transport, and no real credential is read or attached in that mode.
        if api_key is not None and (
                not isinstance(api_key, str) or not api_key.strip() or
                any(character in api_key for character in "\r\n")):
            raise OpenRouterAuthMissing()
        credential = (None if self._insecure_test_transport else
                      (api_key if api_key is not None else self._credential()))
        body = None if payload is None else json.dumps(payload, separators=(",", ":"),
                                                        ensure_ascii=True).encode("utf-8")
        if body is not None and len(body) > self.config.max_request_bytes:
            raise OpenRouterResponseTooLarge()
        effective_timeout = (float(self.config.timeout_seconds)
                             if timeout_seconds is None else timeout_seconds)
        if (not isinstance(effective_timeout, (int, float)) or
                isinstance(effective_timeout, bool) or
                not math.isfinite(effective_timeout) or effective_timeout <= 0):
            raise OpenRouterMalformedResponse()
        effective_timeout = min(float(self.config.timeout_seconds),
                                float(effective_timeout))
        response_limit = (self.config.max_response_bytes
                          if max_response_bytes is None else max_response_bytes)
        if (not isinstance(response_limit, int) or isinstance(response_limit, bool) or
                response_limit < 1 or response_limit > self.config.max_response_bytes):
            raise OpenRouterMalformedResponse()
        request = urllib.request.Request(
            self.config.base_url.rstrip("/") + path,
            data=body, headers=self._headers(credential), method=method)
        # Deliberately remove the local reference before returning; no adapter
        # field ever receives either credential, request, or prompt content.
        try:
            response = self._urlopen(request, timeout=effective_timeout)
            try:
                status = getattr(response, "status", None)
                if status is None:
                    status = response.getcode() if hasattr(response, "getcode") else 200
                try:
                    raw = response.read(response_limit + 1)
                except TypeError:
                    # Small deterministic fakes sometimes expose read() with
                    # no size argument.  Length is checked immediately below.
                    raw = response.read()
                final_url = response.geturl() if hasattr(response, "geturl") else None
                if final_url is not None and _origin(final_url) != _origin(self.config.base_url):
                    raise OpenRouterRedirectError()
            finally:
                close = getattr(response, "close", None)
                if callable(close):
                    close()
        except urllib.error.HTTPError as exc:
            if 300 <= exc.code < 400:
                raise OpenRouterRedirectError() from None
            if exc.code in (401, 403):
                raise OpenRouterAuthError() from None
            if exc.code == 429:
                raise ProviderRateLimit() from None
            raise OpenRouterError() from None
        except (builtins.TimeoutError, socket.timeout):
            raise ProviderTimeout() from None
        except urllib.error.URLError:
            raise ProviderNetworkError() from None
        except (ConnectionError, OSError):
            raise ProviderNetworkError() from None
        except TypeError:
            raise OpenRouterNetworkError() from None
        if not isinstance(raw, (bytes, bytearray)) or len(raw) > response_limit:
            raise OpenRouterResponseTooLarge()
        if status in (401, 403):
            raise OpenRouterAuthError()
        if status == 429:
            raise ProviderRateLimit()
        if isinstance(status, int) and 300 <= status < 400:
            raise OpenRouterRedirectError()
        if isinstance(status, int) and status >= 400:
            raise OpenRouterError()
        try:
            decoded = json.loads(bytes(raw).decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError):
            raise OpenRouterMalformedResponse() from None
        if not isinstance(decoded, Mapping):
            raise OpenRouterMalformedResponse()
        if isinstance(decoded.get("error"), Mapping):
            error = decoded["error"]
            if str(error.get("code", "")) == "429" or "rate" in str(error.get("type", "")).lower():
                raise ProviderRateLimit()
            if "refus" in str(error.get("type", "")).lower():
                raise ProviderRefusal()
            if str(error.get("code", "")) in ("401", "403"):
                raise OpenRouterAuthError()
            raise OpenRouterError()
        return decoded

    def discover(self, *, free_only: bool = False,
                 timeout_seconds: Optional[float] = None) -> list[ModelSpec]:
        payload = self._json_request(
            "/api/v1/models", timeout_seconds=timeout_seconds)
        models = payload.get("data")
        if not isinstance(models, list):
            raise OpenRouterMalformedResponse()
        result = []
        for item in models:
            if not isinstance(item, Mapping) or not isinstance(item.get("id"), str) or not item["id"]:
                raise OpenRouterMalformedResponse()
            supported = item.get("supported_parameters", ())
            if supported is None:
                supported = ()
            if not isinstance(supported, (list, tuple)):
                raise OpenRouterMalformedResponse()
            architecture = item.get("architecture") or {}
            if not isinstance(architecture, Mapping):
                raise OpenRouterMalformedResponse()
            input_modalities = architecture.get("input_modalities", ()) or ()
            output_modalities = architecture.get("output_modalities", ()) or ()
            if not all(isinstance(value, str) for value in (*input_modalities, *output_modalities, *supported)):
                raise OpenRouterMalformedResponse()
            capabilities = frozenset(str(value) for value in (*input_modalities, *output_modalities, *supported))
            tools = frozenset(value for value in supported if value in ("tools", "tool_choice", "functions", "function_call"))
            context = item.get("context_length", item.get("context_window", 0))
            if not isinstance(context, int) or isinstance(context, bool) or context < 0:
                raise OpenRouterMalformedResponse()
            pricing = item.get("pricing") or {}
            if not isinstance(pricing, Mapping):
                raise OpenRouterMalformedResponse()
            prompt_price = _number(pricing.get("prompt"))
            completion_price = _number(pricing.get("completion"))
            if prompt_price is None or completion_price is None or prompt_price < 0 or completion_price < 0:
                raise OpenRouterMalformedResponse()
            free = prompt_price == 0 and completion_price == 0
            spec = ModelSpec(
                self.provider, item["id"], capabilities=capabilities, tools=tools,
                context_window=context, cost_per_1k_tokens=(prompt_price + completion_price) * 1000,
                free=free, credential_env=self.config.api_key_env,
            )
            if not free_only or spec.free:
                result.append(spec)
        return result

    discover_models = discover
    models = discover
    catalog = discover

    def complete(self, model: str, prompt: str, *, request: Any = None,
                 api_key: Optional[str] = None,
                 timeout_seconds: Optional[float] = None) -> OpenRouterResponse:
        if not isinstance(model, str) or not model or not isinstance(prompt, str):
            raise OpenRouterMalformedResponse()
        # Bound prompt material before constructing the JSON request body.
        if len(prompt.encode("utf-8")) > self.config.max_request_bytes:
            raise OpenRouterResponseTooLarge()
        max_output_tokens = getattr(
            request, "max_output_tokens", self.config.default_max_output_tokens)
        if (not isinstance(max_output_tokens, int) or
                isinstance(max_output_tokens, bool) or
                not 1 <= max_output_tokens <= 65536):
            raise OpenRouterMalformedResponse()
        if timeout_seconds is not None and (
                not isinstance(timeout_seconds, (int, float)) or
                isinstance(timeout_seconds, bool) or
                not math.isfinite(timeout_seconds) or timeout_seconds <= 0):
            raise OpenRouterMalformedResponse()
        request_latency_ms = getattr(request, "max_latency_ms", None)
        if request_latency_ms is not None:
            if (not isinstance(request_latency_ms, (int, float)) or
                    isinstance(request_latency_ms, bool) or
                    not math.isfinite(request_latency_ms) or request_latency_ms <= 0):
                raise OpenRouterMalformedResponse()
            request_timeout = float(request_latency_ms) / 1000.0
            timeout_seconds = (request_timeout if timeout_seconds is None
                               else min(float(timeout_seconds), request_timeout))
        response_limit = min(
            self.config.max_response_bytes,
            max(4096, max_output_tokens * 64 + 16384),
        )
        started = time.monotonic()
        payload = self._json_request(
            "/api/v1/chat/completions", method="POST",
            payload={"model": model, "messages": [{"role": "user", "content": prompt}],
                     "max_tokens": max_output_tokens},
            timeout_seconds=timeout_seconds,
            max_response_bytes=response_limit,
            api_key=api_key)
        latency_ms = (time.monotonic() - started) * 1000
        choices = payload.get("choices")
        if not isinstance(choices, list) or not choices or not isinstance(choices[0], Mapping):
            raise OpenRouterMalformedResponse()
        message = choices[0].get("message")
        if not isinstance(message, Mapping):
            raise OpenRouterMalformedResponse()
        if message.get("refusal") or message.get("refused"):
            raise ProviderRefusal()
        content = message.get("content")
        if isinstance(content, list):
            content = "".join(part.get("text", "") for part in content
                               if isinstance(part, Mapping) and isinstance(part.get("text"), str))
        if not isinstance(content, str):
            raise OpenRouterMalformedResponse()
        usage = payload.get("usage")
        if not isinstance(usage, Mapping):
            raise OpenRouterMalformedResponse()
        for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
            value = usage.get(name)
            if (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                raise OpenRouterMalformedResponse()
        completion_tokens = usage["completion_tokens"]
        if completion_tokens > max_output_tokens:
            raise OpenRouterResponseTooLarge()
        if content and completion_tokens == 0:
            raise OpenRouterMalformedResponse()
        if len(content.encode("utf-8")) > max_output_tokens * 64:
            raise OpenRouterResponseTooLarge()
        actual_model = payload.get("model")
        if (not isinstance(actual_model, str) or not actual_model.strip() or
                len(actual_model) > 512):
            raise OpenRouterMalformedResponse()
        raw_cost = usage.get("cost", payload.get("cost"))
        cost = _number(raw_cost) if raw_cost is not None else None
        if raw_cost is not None and (cost is None or not math.isfinite(cost) or cost < 0):
            raise OpenRouterMalformedResponse()
        return OpenRouterResponse(
            output=content,
            input_tokens=usage["prompt_tokens"],
            output_tokens=completion_tokens,
            total_tokens=usage["total_tokens"],
            cost_usd=cost,
            latency_ms=latency_ms,
            actual_model=actual_model,
        )


# Kept as a private-compatible alias for fakes/users that want the safe class.
OpenRouterNetworkError = ProviderNetworkError
OpenRouterAdapter = OpenRouterProvider
OpenRouterModelProvider = OpenRouterProvider
OpenRouter = OpenRouterProvider


__all__ = [
    "OpenRouterAuthError", "OpenRouterAuthMissing", "OpenRouterConfig",
    "OpenRouterError", "OpenRouterMalformedResponse", "OpenRouterProvider",
    "OpenRouterRedirectError",
    "OpenRouterResponse", "OpenRouterResponseTooLarge", "OpenRouterAdapter",
    "OpenRouterModelProvider", "OpenRouter",
]
