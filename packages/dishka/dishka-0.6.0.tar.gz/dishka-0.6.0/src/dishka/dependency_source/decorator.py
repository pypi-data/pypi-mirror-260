from collections.abc import (
    Callable,
)
from typing import (
    Any,
    overload,
)

from dishka.entities.component import Component
from dishka.entities.key import DependencyKey
from dishka.entities.scope import BaseScope
from .factory import Factory, make_factory


class Decorator:
    __slots__ = ("provides", "factory")

    def __init__(self, factory: Factory):
        self.factory = factory
        self.provides = factory.provides

    def as_factory(
            self, *,
            scope: BaseScope,
            new_dependency: DependencyKey,
            cache: bool,
            component: Component,
    ) -> Factory:
        return Factory(
            scope=scope,
            source=self.factory.source,
            provides=self.factory.provides.with_component(component),
            is_to_bind=self.factory.is_to_bind,
            dependencies=[
                (
                    new_dependency
                    if dep.type_hint == self.provides.type_hint
                    else dep
                ).with_component(component)
                for dep in self.factory.dependencies
            ],
            type_=self.factory.type,
            cache=cache,
        )

    def __get__(self, instance, owner):
        return Decorator(self.factory.__get__(instance, owner))


@overload
def decorate(
        *,
        provides: Any = None,
) -> Callable[[Callable], Decorator]:
    ...


@overload
def decorate(
        source: Callable | type,
        *,
        provides: Any = None,
) -> Decorator:
    ...


def decorate(
        source: Callable | type | None = None,
        provides: Any = None,
) -> Decorator | Callable[[Callable], Decorator]:
    if source is not None:
        return Decorator(make_factory(
            provides=provides, scope=None, source=source, cache=False,
        ))

    def scoped(func):
        return Decorator(make_factory(
            provides=provides, scope=None, source=func, cache=False,
        ))

    return scoped
