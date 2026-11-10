"""Alap kiejtési szótár: fizikusok, mértékegységek és gyakori idegen nevek magyar kiejtése.

Használat:  uv run python scripts/seed_lexicon.py
A már meglévő bejegyzéseket felülírja azonos írott alak esetén, a többit nem érinti.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.state import AppState

# írott alak -> kiejtés (kis- és nagybetű érzékeny, hogy a "watt" köznévként ne változzon)
NAMES = {
    "Ampère": "amper", "Biot": "bió", "Bohr": "bór", "Boltzmann": "bolcman", "Celsius": "celziusz",
    "Clausius": "klauziusz", "Coulomb": "kulomb", "Curie": "küri", "Debye": "döbáj", "Descartes": "dékárt",
    "Einstein": "ajnstájn", "Euler": "ojler", "Faraday": "faradéj", "Fourier": "furié", "Gauss": "gausz",
    "Hall": "hól", "Hamilton": "hemilton", "Heaviside": "hevisájd", "Heisenberg": "hájzenberg",
    "Helmholtz": "helmholc", "Henry": "henri", "Hertz": "herc", "Hooke": "húk", "Huygens": "hajhensz",
    "Joule": "dzsúl", "Kelvin": "kelvin", "Kirchhoff": "kirhhoff", "Lagrange": "lagranzs",
    "Laplace": "laplasz", "Larmor": "larmor", "Lenz": "lenc", "Lorentz": "lorenc", "Lorenz": "lorenc",
    "Maxwell": "mekszvel", "Meissner": "májszner", "Mossotti": "moszotti", "Neumann": "nojmann",
    "Newton": "nyúton", "Norton": "norton", "Oersted": "örszted", "Ørsted": "örszted", "Ohm": "óm",
    "Pascal": "paszkál", "Pauli": "pauli", "Planck": "plank", "Poisson": "poaszon", "Poynting": "pojnting",
    "Rowland": "róland", "Savart": "szavár", "Schrödinger": "srődinger", "Siemens": "szímensz",
    "Stokes": "sztoksz", "Tesla": "tesla", "Thévenin": "tevenen", "Thomson": "tomszon", "Volta": "volta",
    "Watt": "vatt", "Weber": "véber", "Weiss": "vájsz", "Wheatstone": "vítsztón", "Zeeman": "zéman",
}

# mértékegységek kiírt alakja (szám nélkül is előfordulnak a szövegben)
UNITS = {
    "coulomb": "kulomb", "joule": "dzsúl", "newton": "nyúton", "weber": "véber", "siemens": "szímensz",
    "watt": "vatt", "hertz": "herc", "pascal": "paszkál", "henry": "henri",
}


def main() -> None:
    st = AppState()
    for written, spoken in NAMES.items():
        st.repo.add_lexicon_entry(written, spoken, True)
    for written, spoken in UNITS.items():
        st.repo.add_lexicon_entry(written, spoken, True)
    print(f"{len(NAMES) + len(UNITS)} bejegyzés a kiejtési szótárban.")


if __name__ == "__main__":
    main()
