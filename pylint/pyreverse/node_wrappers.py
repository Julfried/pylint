# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Wrappers for astroid nodes to support type hinting for Pyreverse."""

from __future__ import annotations

import collections
from dataclasses import dataclass, field
from typing import Any

from astroid import nodes


@dataclass
class NodeWrapper:
    """Base class for node wrappers.

    Allows adding attributes to nodes with proper type hinting.
    """

    node: nodes.NodeNG
    locals_type: dict[str, list[Any]] = field(
        default_factory=lambda: collections.defaultdict(list)
    )
    uid: int | None = None


@dataclass
class ModuleWrapper(NodeWrapper):
    """Wrapper for module nodes."""

    depends: list[str] = field(default_factory=list)
    type_depends: list[str] = field(default_factory=list)


@dataclass
class ClassWrapper(NodeWrapper):
    """Wrapper for class nodes."""

    instance_attrs_type: dict[str, list[Any]] = field(
        default_factory=lambda: collections.defaultdict(list)
    )
    aggregations_type: dict[str, list[Any]] = field(
        default_factory=lambda: collections.defaultdict(list)
    )
    associations_type: dict[str, list[Any]] = field(
        default_factory=lambda: collections.defaultdict(list)
    )
    specializations: list[nodes.ClassDef] = field(default_factory=list)


@dataclass
class FunctionWrapper(NodeWrapper):
    """Wrapper for function nodes."""


class NodeWrapperRegistry:
    """Registry for node wrappers.

    Tracks wrappers for nodes and provides methods to get or create wrappers.
    """

    def __init__(self) -> None:
        self._wrappers: dict[nodes.NodeNG, NodeWrapper] = {}

    def get_wrapper(self, node: nodes.NodeNG) -> NodeWrapper:
        """Get the wrapper for a node, creating it if needed."""
        if node not in self._wrappers:
            if isinstance(node, nodes.Module):
                self._wrappers[node] = ModuleWrapper(node)
            elif isinstance(node, nodes.ClassDef):
                self._wrappers[node] = ClassWrapper(node)
            elif isinstance(node, nodes.FunctionDef):
                self._wrappers[node] = FunctionWrapper(node)
            else:
                self._wrappers[node] = NodeWrapper(node)
        return self._wrappers[node]

    def get_module_wrapper(self, node: nodes.Module) -> ModuleWrapper:
        """Get the wrapper for a module node, creating it if needed."""
        wrapper = self.get_wrapper(node)
        assert isinstance(wrapper, ModuleWrapper)
        return wrapper

    def get_class_wrapper(self, node: nodes.ClassDef) -> ClassWrapper:
        """Get the wrapper for a class node, creating it if needed."""
        wrapper = self.get_wrapper(node)
        assert isinstance(wrapper, ClassWrapper)
        return wrapper

    def get_function_wrapper(self, node: nodes.FunctionDef) -> FunctionWrapper:
        """Get the wrapper for a function node, creating it if needed."""
        wrapper = self.get_wrapper(node)
        assert isinstance(wrapper, FunctionWrapper)
        return wrapper
