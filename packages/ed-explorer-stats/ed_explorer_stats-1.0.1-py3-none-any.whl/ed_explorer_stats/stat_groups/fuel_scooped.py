from . import collector
from .. import time_formatting
from ..colors import TITLE, SECTION, STAT, RESET


def new_collector():
    return FuelScooped()


def get_description():
    return "Total fuel scooped and time spent scooping"


def setup_parser(parser):
    pass


# array of arrays, index corresponds to fuel scoop class which has an array from rating E-A.
# scoop rates are in tonnes per second
_scoop_rates = [
    [0.018, 0.024, 0.030, 0.036, 0.042],
    [0.032, 0.043, 0.054, 0.065, 0.075],
    [0.075, 0.100, 0.126, 0.151, 0.176],
    [0.147, 0.196, 0.245, 0.294, 0.343],
    [0.247, 0.330, 0.412, 0.494, 0.577],
    [0.376, 0.502, 0.627, 0.752, 0.878],
    [0.534, 0.712, 0.890, 1.068, 1.245],
    [0.720, 0.960, 1.200, 1.440, 1.680],
]


class FuelScooped(collector.Collector):
    last_fuelscoop_rate = None
    total_fuel_scooped = 0
    time_scooping = 0

    def __init__(self):
        super().__init__()

    def process_event(self, event):
        if event["event"] == "Loadout":
            for module in event["Modules"]:
                item_name = module["Item"]
                
                if "fuelscoop" in item_name:
                    self.last_fuelscoop_rate = self.get_scoop_rate(item_name)
                    break
            
            return
        
        if event["event"] != "FuelScoop":
            return
        
        fuel_scooped = event["Scooped"]
        
        self.total_fuel_scooped += fuel_scooped
        self.time_scooping += fuel_scooped / self.last_fuelscoop_rate

    def get_output(self):
        self.add_line(f"{TITLE}Fuel scooped\n")
        
        self.add_line(f"{SECTION}Total fuel scooped{RESET}: {STAT}{round(self.total_fuel_scooped)} tonnes")
        self.add_line(f"{SECTION}Time spent scooping{RESET}: {STAT}{time_formatting.format_period(self.time_scooping)}")
        
        return self._output

    def get_scoop_rate(self, full_name):
        size = int(full_name[len("int_fuelscoop_size")])
        class_rating = int(full_name[-1])
        
        return _scoop_rates[size - 1][class_rating - 1]
