from bus.event_bus import bus
from events.events import *
class PublisherAgent:
    def __init__(self): bus.subscribe(JOB_VALIDATED,self.handle)
    def handle(self,j): print(f"Published {j['company']} {j['role']}")
