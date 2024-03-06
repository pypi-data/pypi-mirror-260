__all__ = [
    "scanned_bodies",
    "visited_systems",
    "most_bodies",
    "orbital_period",
    "rotation_period",
    "radius",
    "gravity",
    "fuel_scooped",
    "biological",
    "surface_scans",
]


def get_module_names():
    return __all__


def get_module(name):
    return globals()[name]
