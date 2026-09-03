"""Durable, policy-first runtime primitives for Product Manager OS.

The package root keeps a deliberately small compatibility surface. Domain,
store, conductor, operations, hooks, skills, migrations, and release APIs live
in their named modules; routing's original public imports remain available
here for existing callers.
"""

__version__ = "0.8.0"

from .routing import (
    Attempt,
    EnvironmentSecrets,
    ModelRouter,
    ModelSpec,
    ProviderError,
    ProviderNetworkError,
    ProviderRateLimit,
    ProviderRefusal,
    ProviderResponse,
    ProviderTimeout,
    ProviderUnavailable,
    ModelUnavailable,
    RateLimitError,
    TimeoutError,
    NetworkError,
    RouteDecision,
    RouteStatus,
    RoutingRequest,
    route_model,
)

__all__ = [
    "__version__",
    "EnvironmentSecrets",
    "Attempt",
    "ModelRouter",
    "ModelSpec",
    "ProviderError",
    "ProviderNetworkError",
    "ProviderRateLimit",
    "ProviderRefusal",
    "ProviderResponse",
    "ProviderTimeout",
    "ProviderUnavailable",
    "ModelUnavailable",
    "RateLimitError",
    "TimeoutError",
    "NetworkError",
    "RouteDecision",
    "RouteStatus",
    "RoutingRequest",
    "route_model",
]
