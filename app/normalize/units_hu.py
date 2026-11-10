"""Mértékegységek szám után (6.3, 9. lépés)."""

UNITS: dict[str, str] = {
    "V": "volt",
    "A": "amper",
    "Ω": "óm",
    "W": "watt",
    "Hz": "hertz",
    "kHz": "kilohertz",
    "MHz": "megahertz",
    "mA": "milliamper",
    "mV": "millivolt",
    "kΩ": "kiloóm",
    "F": "farad",
    "µF": "mikrofarad",
    "μF": "mikrofarad",
    "nF": "nanofarad",
    "H": "henri",
    "mH": "millihenri",
    "s": "másodperc",
    "ms": "milliszekundum",
    "m": "méter",
    "cm": "centiméter",
    "mm": "milliméter",
    "km": "kilométer",
    "kg": "kilogramm",
    "g": "gramm",
    "°C": "celsius-fok",
    "K": "kelvin",
    "%": "százalék",
    "Ft": "forint",
    "€": "euró",
    "$": "dollár",
}

# Hosszabb jelek előre, hogy a `kΩ` ne `k` + `Ω`-ként illeszkedjen.
UNIT_KEYS = sorted(UNITS, key=len, reverse=True)
