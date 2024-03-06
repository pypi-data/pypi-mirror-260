from . import collector
from ..colors import TITLE, SECTION, TYPE, STAT, RESET


def new_collector():
    return Biological()


def get_description():
    return "All exobiology on-foot scans by genus and species"


def setup_parser(parser):
    pass


class Biological(collector.Collector):
    scanned_genus = None
    latest_localisation = None
    total = 0

    def __init__(self):
        super().__init__()
        
        self.scanned_genus = {}
        self.latest_localisation = {}

    def process_event(self, event):
        if event["event"] != "ScanOrganic":
            return
        if event["ScanType"] != "Analyse":
            return
        
        self.total += 1
        
        genus_id = event["Genus"]
        genus_name = event["Genus_Localised"]
        species_id = event["Species"]
        species_name = event["Species_Localised"]
        
        self.latest_localisation[genus_id] = genus_name
        self.latest_localisation[species_id] = species_name
        
        if genus_id not in self.scanned_genus:
            self.scanned_genus[genus_id] = {
                species_id: 1
            }
        
        if species_id not in self.scanned_genus[genus_id]:
            self.scanned_genus[genus_id][species_id] = 0
        
        self.scanned_genus[genus_id][species_id] += 1

    def get_output(self):
        self.add_line(f"{TITLE}Biological data\n")
        self.add_line(f"Total analysed: {STAT}{self.total}\n")
        
        for genus_id in self.scanned_genus:
            genus_total = 0
            for species_id in self.scanned_genus[genus_id]:
                genus_total += self.scanned_genus[genus_id][species_id]
            
            genus_name = self.latest_localisation[genus_id]
            self.add_line(f"{SECTION}{genus_name} genus{RESET} ({STAT}{genus_total}{RESET} total)")
            
            for species_id in self.scanned_genus[genus_id]:
                species_name = self.latest_localisation[species_id]
                self.add_line(f"\t{TYPE}{species_name}{RESET}: {STAT}{self.scanned_genus[genus_id][species_id]}{RESET} analysed")
        
        return self._output
