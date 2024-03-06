from . import collector
from .. import stellar_info
from ..colors import TITLE, SECTION, TYPE, STAT, RESET


def new_collector():
    return ScannedBodies()


def get_description():
    return "Counts of all scanned stellar bodies"


def setup_parser(parser):
    pass


class ScannedBodies(collector.Collector):
    bodies_scanned = None
    planet_classes_scanned = None
    star_types_scanned = None
    total = 0

    def __init__(self):
        super().__init__()
        
        self.bodies_scanned = set()
        self.planet_classes_scanned = {}
        self.star_types_scanned = {}

    def process_event(self, event):
        if event["event"] != "Scan":
            return
        if "PlanetClass" not in event and "StarType" not in event:
            return
        if event["BodyName"] in self.bodies_scanned:
            return
        
        self.bodies_scanned.add(event["BodyName"])
        self.total += 1
        
        if "PlanetClass" in event:
            planet_class = event["PlanetClass"]
            
            if planet_class not in self.planet_classes_scanned:
                self.planet_classes_scanned[planet_class] = 0
            
            self.planet_classes_scanned[planet_class] += 1
        elif "StarType" in event:
            star_type = event["StarType"]
            
            if star_type not in self.star_types_scanned:
                self.star_types_scanned[star_type] = 0
            
            self.star_types_scanned[star_type] += 1

    def get_stellar_remnant_names(self):
        names = {}
    
        for type in stellar_info.stellar_remnant_types():
            names[stellar_info.type_to_name(type)] = type
        
        return names

    def get_output(self):
        self.add_line(f"{TITLE}Scanned bodies\n")
        self.add_line(f"Total: {STAT}{self.total}\n")
        
        self.add_line(f"{SECTION}Stellar remnants:")
        stellar_remnant_names = self.get_stellar_remnant_names()
        for name in sorted(stellar_remnant_names):
            type = stellar_remnant_names[name]
            count = self.star_types_scanned.get(type, 0)
            self.add_line(f"\t{TYPE}{name}{RESET}: {STAT}{count}")
            
            if type in self.star_types_scanned:
                del self.star_types_scanned[type]
        
        self.add_line(f"{SECTION}Main sequence stars:")
        for type in ["O", "B", "A", "F", "G", "K", "M"]:
            self.add_line(f"\t{TYPE}{type} star{RESET}: {STAT}{self.star_types_scanned.get(type, 0)}")
            
            if type in self.star_types_scanned:
                del self.star_types_scanned[type]
        
        self.add_line(f"{SECTION}Dwarf stars:")
        for type in ["Y", "T", "L"]:
            self.add_line(f"\t{TYPE}{type} brown dwarf{RESET}: {STAT}{self.star_types_scanned.get(type, 0)}")
            
            if type in self.star_types_scanned:
                del self.star_types_scanned[type]
        
        self.add_line(f"{SECTION}Other:")
        for type in sorted(self.star_types_scanned):
            name = stellar_info.type_to_name(type)
            self.add_line(f"\t{TYPE}{name}{RESET}: {STAT}{self.star_types_scanned[type]}")
        
        self.add_line(f"{SECTION}Planets:")
        for planet_class in sorted(self.planet_classes_scanned):
            self.add_line(f"\t{TYPE}{planet_class}{RESET}: {STAT}{self.planet_classes_scanned[planet_class]}")
        
        return self._output
