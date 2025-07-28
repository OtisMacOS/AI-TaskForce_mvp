from .chiefmind import ChiefMindAgent
from .taskplanner import TaskPlannerAgent
from .researcher import ResearcherAgent
from .prdwriter import PRDWriterAgent
from .toolfinder import ToolFinderAgent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from llm_module import create_llm_function

class AgentFactory:
    def __init__(self, llm=None):
        self.llm = llm or create_llm_function()

    def get_agent(self, agent_type: str):
        if agent_type == "chiefmind":
            return ChiefMindAgent(self.llm)
        elif agent_type == "taskplanner":
            return TaskPlannerAgent(self.llm)
        elif agent_type == "researcher":
            return ResearcherAgent(self.llm)
        elif agent_type == "prdwriter":
            return PRDWriterAgent(self.llm)
        elif agent_type == "toolfinder":
            return ToolFinderAgent(self.llm)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}") 