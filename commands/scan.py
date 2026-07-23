from bus.event_bus import bus
from events.events import SCAN_REQUEST
def run(): bus.publish(SCAN_REQUEST,{})
