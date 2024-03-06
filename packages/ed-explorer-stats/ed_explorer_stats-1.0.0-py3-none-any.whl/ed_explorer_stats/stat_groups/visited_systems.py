from . import collector
from ..colors import TITLE, STAT

def new_collector():
    return VisitedSystems()


def get_description():
    return "Total systems visited"


def setup_parser(parser):
    pass


class VisitedSystems(collector.Collector):
    visited_systems = None

    def __init__(self):
        super().__init__()
        
        self.visited_systems = set()

    def process_event(self, event):
        if event["event"] != "Scan" and event["event"] != "Location" and event["event"] != "FSDJump":
            return
            
        self.visited_systems.add(event["StarSystem"])

    def get_output(self):
        self.add_line(f"{TITLE}Visited systems")
        self.add_line(f"\tTotal visited systems: {STAT}{len(self.visited_systems)}")
        
        return self._output
    