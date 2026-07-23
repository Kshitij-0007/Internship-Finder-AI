from collections import defaultdict
class EventBus:
    def __init__(self): self.s=defaultdict(list)
    def subscribe(self,e,h): self.s[e].append(h)
    def publish(self,e,p):
        [h(p) for h in self.s[e]]
bus=EventBus()
