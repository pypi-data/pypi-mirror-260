_star_type_names = {
    "N": "Neutron star",
    "W": "Wolf-Rayet star (W)",
    "WN": "Wolf-Rayet star (WN)",
    "WNC": "Wolf-Rayet star (WNC)",
    "WC": "Wolf-Rayet star (WC)",
    "WO": "Wolf-Rayet star (WO)",
    "TTS": "T Tauri star",
    "AeBe": "Herbig Ae/Be star",
    "T": "T brown dwarf",
    "L": "L brown dwarf",
    "Y": "Y brown dwarf",
    "O": "O star",
    "B": "B star",
    "B_BlueWhiteSuperGiant": "B blue-white supergiant star",
    "A": "A star",
    "F": "F star",
    "F_WhiteSuperGiant": "F white supergiant star",
    "G": "G star",
    "G_WhiteSuperGiant": "G white supergiant star",
    "K": "K star",
    "K_OrangeGiant": "K orange giant star",
    "M": "M star",
    "M_RedGiant": "M red giant star",
    "M_RedSuperGiant": "M red supergiant star",
    "S": "S star",
    "MS": "MS star",
    "C": "Carbon star (C)",
    "CS": "Carbon star (C)",
    "CN": "Carbon star (C)",
    "CJ": "Carbon star (C)",
    "CH": "Carbon star (C)",
    "CHd": "Carbon star (C)",
    "H": "Black hole",
    "SupermassiveBlackHole": "Supermassive black hole",
    "D":    "White dwarf (D)",
    "DA":   "White dwarf (DA)",
    "DAB":  "White dwarf (DAB)",
    "DAO":  "White dwarf (DAO)",
    "DAZ":  "White dwarf (DAZ)",
    "DAV":  "White dwarf (DAV)",
    "DB":   "White dwarf (DB)",
    "DBZ":  "White dwarf (DBZ)",
    "DBV":  "White dwarf (DBV)",
    "DO":   "White dwarf (DO)",
    "DOV":  "White dwarf (DOV)",
    "DQ":   "White dwarf (DQ)",
    "DC":   "White dwarf (DC)",
    "DCV":  "White dwarf (DCV)",
    "DX":   "White dwarf (DX)",
}


def type_to_name(type: str) -> str:
    if not type:
        return f"Invalid type: {type}"

    if type in _star_type_names:
        return _star_type_names[type]
    
    return f"Unknown type '{type}'"


def sorted_types() -> list[str]:
    return [
        "O",
        "B", "B_BlueWhiteSuperGiant",
        "A",
        "F", "F_WhiteSuperGiant",
        "G", "G_WhiteSuperGiant",
        "K", "K_OrangeGiant",
        "M", "M_RedGiant", "M_RedSuperGiant",
        "T", "L", "Y",
        "N",
        "H", "SupermassiveBlackHole",
        "D", "DA", "DAB", "DAO", "DAZ", "DAV", "DB", "DBZ", "DBV", "DC", "DCV", "DO", "DOV", "DQ", "DX",
        "W", "WN", "WNC", "WC", "WO",
        "TTS",
        "AeBe",
        "S", "MS",
        "C", "CS", "CN", "CJ", "CH", "CHd",
    ]


def star_types() -> list[str]:
    return list(_star_type_names.keys())


def stellar_remnant_types() -> set[str]:
    types = set()
    white_dwarf_types = ["D", "DA", "DAB", "DAO", "DAZ", "DAV", "DB", "DBZ", "DBV",
                         "DO", "DOV", "DQ", "DC", "DCV", "DX"]
    
    types.update(white_dwarf_types)
    types.add("H")
    types.add("N")
    types.add("SupermassiveBlackHole")
    
    return types
