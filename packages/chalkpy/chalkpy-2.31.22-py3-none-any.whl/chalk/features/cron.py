from __future__ import annotations

import inspect
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Collection, Optional, Union

from chalk.utils.duration import CronTab, Duration

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference


@dataclass
class CronQuery:
    name: str
    cron: CronTab | Duration
    output: Collection[str]
    max_samples: Optional[int]
    recompute_features: Union[bool, Collection[str]]
    lower_bound: Optional[datetime]
    upper_bound: Optional[datetime]
    tags: Collection[str]
    required_resolver_tags: Collection[str]
    filename: str


CRON_QUERY_REGISTRY: dict[str, CronQuery] = {}


def cron_query(
    name: str,
    schedule: CronTab | Duration,
    output: Collection[FeatureReference],
    max_samples: Optional[int] = None,
    recompute_features: Union[bool, Collection[FeatureReference]] = True,
    lower_bound: Optional[datetime] = None,
    upper_bound: Optional[datetime] = None,
    tags: Optional[Collection[str]] = None,
    required_resolver_tags: Optional[Collection[str]] = None,
) -> None:
    # TODO: we might want to specify "cache_features" instead of "recompute_features"
    # we might want to specify a list of "allowed_resolvers" instead of "required_resolver_tags"

    if name in CRON_QUERY_REGISTRY:
        raise ValueError(f"Cron query with name {name} already exists. Cron names must be unique.")

    if len(output) == 0:
        raise ValueError(f"Cron query does not require any outputs. Chalk will not run it.")

    if tags is None:
        tags = []
    if required_resolver_tags is None:
        required_resolver_tags = []
    if lower_bound is not None:
        lower_bound = lower_bound.astimezone(tz=timezone.utc)
    if upper_bound is not None:
        upper_bound = upper_bound.astimezone(tz=timezone.utc)

    caller_filename = inspect.stack()[1].filename

    CRON_QUERY_REGISTRY[name] = CronQuery(
        name=name,
        cron=schedule,
        output=[str(f) for f in output],
        max_samples=max_samples,
        recompute_features=(
            recompute_features
            if recompute_features is True or recompute_features is False
            else [str(f) for f in recompute_features]
        ),
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        tags=tags,
        required_resolver_tags=required_resolver_tags,
        filename=caller_filename,
    )
