"""Data test.

Every file under tests/data is validated against the schema with the LinkML validator. The
target class is the file name up to the first "-".

- valid/            must validate
- invalid/          must fail, and every `# expect: <regex>` header line must match an error
- problem/invalid/  should fail but passes today (strict xfail: an XPASS means move it to invalid/)
- problem/valid/    should validate but is rejected today with the `# expect:` errors (strict xfail)
"""

import re
from pathlib import Path

import pytest
import yaml
from linkml.validator import validate
from linkml_runtime.loaders import yaml_loader

import rapid_cp_schema.datamodel.rapid_cp_schema

SCHEMA = Path(__file__).parent.parent / "src" / "rapid_cp_schema" / "schema" / "rapid_cp_schema.yaml"
DATA_DIR = Path(__file__).parent / "data"

EXPECT = re.compile(r"^#\s*expect:\s*(.+?)\s*$", re.MULTILINE)


def files(subdir):
    return sorted((DATA_DIR / subdir).glob("*.yaml"))


def ids(paths):
    return [p.stem for p in paths]


def target_class(path):
    return path.stem.split("-")[0]


def errors(path):
    instance = yaml.safe_load(path.read_text())
    report = validate(instance, str(SCHEMA), target_class(path))
    return [r.message for r in report.results]


VALID = files("valid")
INVALID = files("invalid")
PROBLEM_INVALID = files("problem/invalid")
PROBLEM_VALID = files("problem/valid")


@pytest.mark.parametrize("filepath", VALID, ids=ids(VALID))
def test_valid_data_files(filepath):
    """Valid files validate and load into the generated dataclasses."""
    assert errors(filepath) == []
    tgt_class = getattr(rapid_cp_schema.datamodel.rapid_cp_schema, target_class(filepath))
    assert yaml_loader.load(str(filepath), target_class=tgt_class)


@pytest.mark.parametrize("filepath", INVALID, ids=ids(INVALID))
def test_invalid_data_files(filepath):
    """Invalid files fail validation, for the reason their `# expect:` lines state."""
    expected = EXPECT.findall(filepath.read_text())
    assert expected, f"{filepath.name} needs at least one '# expect: <regex>' header line"
    messages = errors(filepath)
    assert messages, "validated, but should have failed"
    for pattern in expected:
        assert any(re.search(pattern, m) for m in messages), f"no error matches {pattern!r}: {messages}"


@pytest.mark.xfail(
    strict=True, raises=AssertionError, reason="schema does not yet reject this; if it passes, move it to invalid/"
)
@pytest.mark.parametrize("filepath", PROBLEM_INVALID, ids=ids(PROBLEM_INVALID))
def test_problem_invalid_data_files(filepath):
    assert errors(filepath)


class KnownRejection(Exception):
    """A problem/valid file is rejected with the errors its `# expect:` lines record."""


@pytest.mark.xfail(
    strict=True, raises=KnownRejection, reason="schema rejects this valid data; if it passes, move it to valid/"
)
@pytest.mark.parametrize("filepath", PROBLEM_VALID, ids=ids(PROBLEM_VALID))
def test_problem_valid_data_files(filepath):
    """Rejected only for the recorded reason; any other error is a real failure, not an xfail."""
    expected = EXPECT.findall(filepath.read_text())
    assert expected, f"{filepath.name} needs '# expect: <regex>' lines recording the current rejection"
    messages = errors(filepath)
    if messages and all(any(re.search(p, m) for m in messages) for p in expected):
        raise KnownRejection(messages)
    assert messages == [], f"rejected for an unrecorded reason: {messages}"
