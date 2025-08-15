# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""For the visitors.diadefs module."""

# pylint: disable=redefined-outer-name

from __future__ import annotations

import os
import warnings
from collections.abc import Generator
from pathlib import Path

import astroid
import pytest

from pylint.pyreverse import inspector
from pylint.pyreverse.inspector import Project
from pylint.testutils.utils import _test_cwd
from pylint.typing import GetProjectCallable

HERE = Path(__file__)
TESTS = HERE.parent.parent


@pytest.fixture
def project(get_project: GetProjectCallable) -> Generator[Project]:
    with _test_cwd(TESTS):
        project = get_project("data", "data")
        linker = inspector.Linker(project)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            with inspector.PyReverseAnalysisContext(linker):
                linker.visit(project)
        yield project


@pytest.fixture
def project_with_linker(
    get_project: GetProjectCallable,
) -> Generator[tuple[Project, inspector.Linker]]:
    with _test_cwd(TESTS):
        project = get_project("data", "data")
        linker = inspector.Linker(project)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            with inspector.PyReverseAnalysisContext(linker):
                linker.visit(project)
        yield project, linker


def test_locals_assignment_resolution(
    project_with_linker: tuple[Project, inspector.Linker],
) -> None:
    project, linker = project_with_linker
    klass = project.get_module("data.clientmodule_test")["Specialization"]
    metadata = linker.metadata_manager.get_metadata(klass)
    type_dict = metadata.locals_type
    assert len(type_dict) == 2
    keys = sorted(type_dict.keys())
    assert keys == ["TYPE", "top"]
    assert len(type_dict["TYPE"]) == 1
    assert type_dict["TYPE"][0].value == "final class"
    assert len(type_dict["top"]) == 1
    assert type_dict["top"][0].value == "class"


def test_instance_attrs_resolution(
    project_with_linker: tuple[Project, inspector.Linker],
) -> None:
    project, linker = project_with_linker
    klass = project.get_module("data.clientmodule_test")["Specialization"]
    metadata = linker.metadata_manager.get_metadata(klass)
    type_dict = metadata.instance_attrs_type
    assert len(type_dict) == 3
    keys = sorted(type_dict.keys())
    assert keys == ["_id", "relation", "relation2"]
    assert isinstance(type_dict["relation"][0], astroid.bases.Instance), type_dict[
        "relation"
    ]
    assert type_dict["relation"][0].name == "DoNothing"
    assert type_dict["_id"][0] is astroid.Uninferable


def test_from_directory(project: Project) -> None:
    expected = os.path.join("tests", "data", "__init__.py")
    assert project.name == "data"
    assert project.path.endswith(expected)


def test_project_node(project: Project) -> None:
    expected = [
        "data",
        "data.clientmodule_test",
        "data.nullable_pattern",
        "data.property_pattern",
        "data.suppliermodule_test",
    ]
    assert sorted(project.keys()) == expected
