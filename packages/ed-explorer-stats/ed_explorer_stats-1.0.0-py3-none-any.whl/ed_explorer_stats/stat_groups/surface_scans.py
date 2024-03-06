from . import collector
from ..colors import TITLE, SECTION, STAT, RESET


def new_collector():
    return SurfaceScans()


def get_description():
    return "DSS probes used and efficiency"


def setup_parser(parser):
    pass


class SurfaceScans(collector.Collector):
    total_probes = 0
    total_bodies = 0
    total_rings = 0
    average_efficiency = 0

    def __init__(self):
        super().__init__()

    def process_event(self, event):
        if event["event"] != "SAAScanComplete":
            return
        
        probes_used = event["ProbesUsed"]
        efficiency_target = event["EfficiencyTarget"]
        
        self.total_probes += probes_used
        
        if efficiency_target != 0:
            self.total_bodies += 1
            self.average_efficiency += probes_used / efficiency_target
        else:
            self.total_rings += 1

    def get_output(self):
        self.add_line(f"{TITLE}Surface scans\n")
        
        self.add_line(f"{SECTION}Total probes hit{RESET}: {STAT}{self.total_probes} probes")
        self.add_line(f"{SECTION}Total bodies scanned{RESET}: {STAT}{self.total_bodies}{RESET}")
        self.add_line(f"{SECTION}Total rings scanned{RESET}: {STAT}{self.total_rings}{RESET}")
        self.add_line(f"{SECTION}Average efficiency{RESET}: {STAT}{round(self.average_efficiency / self.total_bodies * 100)}%{RESET} of target efficiency")
        
        return self._output
