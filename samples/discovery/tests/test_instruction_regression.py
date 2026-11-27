"""Regression test for the SKILL.md + references/ split in samples/discovery.

Loads instruction.py directly by file path (bypassing package-relative
imports and agent.py's google-adk/Dataplex imports, which this test has no
need of and which would otherwise require live credentials to import). The
assertions check that every piece of behavior-relevant content from the
pre-split, monolithic SKILL.md is still present in the concatenated
instruction that the agent actually receives — i.e. that splitting the file
for maintainability did not drop or alter what the model is told.
"""

import importlib.util
import os

import pytest

_DISCOVERY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_instruction_module():
  spec = importlib.util.spec_from_file_location(
      'instruction', os.path.join(_DISCOVERY_DIR, 'instruction.py')
  )
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


@pytest.fixture(scope='module')
def instruction_text():
  return _load_instruction_module().load_instruction()


# Every predicate row that existed in the original, pre-split SKILL.md.
PREDICATE_ROWS = ['type', 'system', 'description', 'name', 'displayname', 'projectid', 'parent']

# Every worked example pair from the original SKILL.md's "Examples" section.
EXAMPLE_PAIRS = [
    ('system=bigquery AND type=table AND name:foo AND projectid=bar'),
    ('type=table AND -name:foo'),
    ('type=table AND (projectid:foo-1 OR projectid:bar-1)'),
    ('type=table AND parent=bar'),
    ('type=dataset'),
    ('((type=table OR type=dataset) AND projectid=foo) OR system=bigquery'),
    ('type=table AND name:sales AND\ndescription=pollution'),
]


def test_predicate_table_rows_all_present(instruction_text):
  for predicate in PREDICATE_ROWS:
    assert f'`{predicate}`' in instruction_text, (
        f'Predicate `{predicate}` missing from concatenated instruction'
    )


def test_output_format_and_adherence_rules_present(instruction_text):
  assert 'NEVER invent a new predicate' in instruction_text
  assert 'AND` and `OR` MUST be in\n    uppercase' in instruction_text
  assert '-name:foo' in instruction_text


def test_all_worked_examples_present(instruction_text):
  for expected_query in EXAMPLE_PAIRS:
    assert expected_query in instruction_text, (
        f'Worked example output {expected_query!r} missing from'
        ' concatenated instruction'
    )


def test_all_steps_present(instruction_text):
  for step_heading in [
      'Step 1: Understand the query',
      'Step 2: Semantic Decomposition & Generating Variations',
      'Step 3: Call Knowledge Catalog Search (Batching)',
      'Step 4: Merge Search Results',
      'Step 5: Identify the best Results',
  ]:
    assert step_heading in instruction_text


def test_baseline_search_rule_present(instruction_text):
  assert 'Baseline Search' in instruction_text
  assert 'word for word' in instruction_text


def test_dedup_uses_stable_entry_name_not_display_name(instruction_text):
  assert 'entry_name' in instruction_text
  assert 'not `display_name`' in instruction_text


def test_references_are_not_duplicated_in_skill_md_itself():
  skill_md_path = os.path.join(_DISCOVERY_DIR, 'SKILL.md')
  with open(skill_md_path, 'r') as f:
    skill_md_text = f.read()
  # The Predicate Reference Table itself should live only in references/,
  # not be duplicated inline in SKILL.md.
  assert '**`displayname`**' not in skill_md_text
  assert 'Example 9' not in skill_md_text
