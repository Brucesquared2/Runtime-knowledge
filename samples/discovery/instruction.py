"""Loads the discovery agent's instruction from SKILL.md plus references/.

Kept free of any google-adk/Dataplex imports (unlike agent.py, which has
module-level side effects on import) so this concatenation logic — the
"legacy adapter" compatibility seam described in docs/skill-design-guide.md
for a harness with no file-reading tool — can be imported and tested in
isolation.
"""

import os

SKILL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'SKILL.md')
REFERENCES_DIR = os.path.join(os.path.dirname(__file__), 'references')


def load_instruction() -> str:
  """Loads the agent instruction from SKILL.md plus its references/ files.

  SKILL.md and references/ are kept as separate files for maintainability
  (see docs/skill-design-guide.md), but this agent has no file-reading tool
  of its own, so all reference content is concatenated into a single
  instruction string at load time. A harness with a file-reading tool could
  instead keep SKILL.md and references/ separate and load the latter on
  demand.
  """
  with open(SKILL_FILE_PATH, 'r') as f:
    instruction = f.read()

  if os.path.isdir(REFERENCES_DIR):
    for filename in sorted(os.listdir(REFERENCES_DIR)):
      reference_path = os.path.join(REFERENCES_DIR, filename)
      with open(reference_path, 'r') as f:
        instruction += '\n\n' + f.read()

  return instruction
