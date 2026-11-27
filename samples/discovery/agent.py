"""Knowledge Catalog Discovery Agent."""

from google.adk.agents import llm_agent
from google.adk.models import google_llm

from . import tools
from .instruction import load_instruction
from .utils import get_consumer_project

consumer_project = get_consumer_project()
GEMINI_MODEL = f"projects/{consumer_project}/locations/global/publishers/google/models/gemini-3-flash-preview"


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
