from typing import (
    Any,
)

from dishka.entities.component import Component
from dishka.entities.key import DependencyKey
from dishka.entities.scope import BaseScope
from .factory import Factory, FactoryType


def _identity(x: Any) -> Any:
    return x


class Alias:
    __slots__ = ("source", "provides", "cache", "component")

    def __init__(
            self, *,
            source: DependencyKey,
            provides: DependencyKey,
            cache: bool,
    ) -> None:
        self.source = source
        self.provides = provides
        self.cache = cache

    def as_factory(
            self, scope: BaseScope, component: Component,
    ) -> Factory:
        return Factory(
            scope=scope,
            source=_identity,
            provides=self.provides.with_component(component),
            is_to_bind=False,
            dependencies=[self.source.with_component(component)],
            type_=FactoryType.ALIAS,
            cache=self.cache,
        )

    def __get__(self, instance, owner):
        return self


def alias(
        *,
        source: type,
        provides: type | None = None,
        cache: bool = True,
        component: Component | None = None,
) -> Alias:
    if component is provides is None:
        raise ValueError("Either component or provides must be set in alias")
    if provides is None:
        provides = source
    return Alias(
        source=DependencyKey(
            type_hint=source,
            component=component,
        ),
        provides=DependencyKey(provides, None),
        cache=cache,
    )
