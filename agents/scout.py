from bus.event_bus import bus
from events.events import *
class ScoutAgent:
    def __init__(self,mcp): self.mcp=mcp; bus.subscribe(SCAN_REQUEST,self.handle)
    def handle(self,_):
        [bus.publish(JOB_DISCOVERED,j) for j in self.mcp.fetch_all_jobs()]
