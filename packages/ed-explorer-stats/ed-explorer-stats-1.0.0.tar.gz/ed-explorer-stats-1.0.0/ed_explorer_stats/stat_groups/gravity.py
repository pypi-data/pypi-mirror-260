from . import min_max_collector
from ..colors import TITLE


def new_collector():
    return Gravity()


def get_description():
    return "The landable planets/moons with the lowest and highest gravity"


def setup_parser(parser):
    pass


class Gravity(min_max_collector.MinMaxCollector):
    def __init__(self):
        super().__init__()

    def process_event(self, event):
        if event["event"] != "Scan":
            return
        if "SurfaceGravity" not in event:
            return
        if "Landable" not in event or not event["Landable"]:
            return
        
        object_info = self.get_object_info(event["BodyName"], event["StarSystem"], event["SurfaceGravity"])
        
        self.check_body(self.notable_bodies, event["PlanetClass"], object_info)

    def get_output(self):
        self.add_line(f"{TITLE}Landable gravity\n")

        for type in sorted(self.notable_bodies):
            self.add_type_info(type, self.notable_bodies[type])
            self.add_line()
        
        return self._output

    def get_formatted_stat(self, stat):
        return f"{round(stat / 9.8, 3)}g"
