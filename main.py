from mcps.careers import CareerMCP
from agents.scout import ScoutAgent
from agents.validator import ValidatorAgent
from agents.publisher import PublisherAgent
from commands.scan import run
m=CareerMCP();ScoutAgent(m);ValidatorAgent();PublisherAgent();
if __name__=='__main__': run()
