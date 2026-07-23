from bus.event_bus import bus
from events.events import *
class ValidatorAgent:
    def __init__(self): bus.subscribe(JOB_DISCOVERED,self.handle)
    def handle(self,j): j['confidence']=95; bus.publish(JOB_VALIDATED,j)
