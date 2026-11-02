"""Knowledge Catalog Discovery Agent."""

import os

from google.adk.agents import llm_agent
from google.adk.models import google_llm

from . import tools
from .utils import get_consumer_project

consumer_project = get_consumer_project()
GEMINI_MODEL = f"projects/{consumer_project}/locations/global/publishers/google/models/gemini-3-flash-preview"

# Path to the skill file and its reference material, relative to agent.py.
SKILL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'SKILL.md')
REFERENCES_DIR = os.path.join(os.path.dirname(__file__), 'references')


def load_instruction() -> str:
  """Loads the agent instruction from SKILL.md plus its references/ files.

  SKILL.md and references/ are kept as separate files for maintainability
  (see docs/skill-design-guide.md), but this agent has no file-reading tool
  of its own, so all reference content is concatenated into a single
  instruction string at load time.
  """
  with open(SKILL_FILE_PATH, 'r') as f:
    instruction = f.read()

  if os.path.isdir(REFERENCES_DIR):
    for filename in sorted(os.listdir(REFERENCES_DIR)):
      reference_path = os.path.join(REFERENCES_DIR, filename)
      with open(reference_path, 'r') as f:
        instruction += '\n\n' + f.read()

  return instruction


discovery_agent = llm_agent.Agent(
    model=google_llm.Gemini(model=GEMINI_MODEL),
    name='knowledge_catalog_discovery_agent',
    description=(
        'Searches Knowledge Catalog for data entries based on Natural Language'
        ' user queries.'
    ),
    instruction=load_instruction(),  # Load instruction from file
    tools=[
        tools.knowledge_catalog_search,
    ],
)
