from . import collector
from ..colors import TYPE, STAT, RESET


class MinMaxCollector(collector.Collector):
    notable_stars = None
    notable_bodies = None
    
    def __init__(self):
        super().__init__()
    
        self.notable_stars = {}
        self.notable_bodies = {}

    def get_formatted_stat(self, stat):
        return stat

    def add_type_info(self, type_name, info):
        self.add_line(str(TYPE) + type_name)
        
        highest_info = info["highest"]
        lowest_info = info["lowest"]
            
        highest_system = highest_info["system"]
        lowest_system = lowest_info["system"]
        
        highest_object = highest_info["name"]
        lowest_object = lowest_info["name"]
        
        highest_formatted = self.get_formatted_stat(highest_info["stat"])
        lowest_formatted = self.get_formatted_stat(lowest_info["stat"])
        
        if highest_info == lowest_info:
            self.add_line(f"\tHighest/lowest: {STAT}{highest_formatted}{RESET} (object {highest_object} in system {highest_system})")
        else:
            self.add_line(f"\tHighest: {STAT}{highest_formatted}{RESET} (object {highest_object} in system {highest_system})")
            self.add_line(f"\tLowest: {STAT}{lowest_formatted}{RESET} (object {lowest_object} in system {lowest_system})")

    def shorten_body_name(self, name, system):
        if name == system:
            return name

        if name.startswith(system):
            return name[len(system) + 1:]

        return name

    def get_object_info(self, object_name, system_name, stat):
        return {
            "name": self.shorten_body_name(object_name, system_name),
            "stat": stat,
            "system": system_name,
        }

    def check_body(self, lookup_dict, type, object_info):
        if type not in lookup_dict:
            lookup_dict[type] = {
                "highest": object_info,
                "lowest": object_info,
            }
        else:
            if lookup_dict[type]["highest"]["stat"] < object_info["stat"]:
                lookup_dict[type]["highest"] = object_info
            if lookup_dict[type]["lowest"]["stat"] > object_info["stat"]:
                lookup_dict[type]["lowest"] = object_info
