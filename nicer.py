import math
import random
import emoji
from enum import Enum
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class Device(Enum):
    WarpEngines = 1
    ShortRangeSensors = 2
    LongRangeSensors = 3
    PhaserControl = 4
    PhotonTubes = 5
    DamageControl = 6
    ShieldControl = 7
    LibraryComputer = 8


class MapObjects(Enum):
    Blank = 0
    Star = 1
    StarBase = 2
    Enterprise = 3
    Klingon = 4


def quadrant_name(pos, quadrant_only=False):
    x = pos[0]
    y = pos[1]

    quadrants = ["ANTARES", "RIGEL", "PROCYON", "VEGA", "CANOPUS", "ALTAIR", "SAGGITARIUS", "POLLUX", "SIRIUS", "DENEB",
                 "CAPELLA", "BETELGEUSE", "ALDEBARAN", "REGULUS", "ARCTURUS", "SPICA"]
    subquadrants = ["I", "II", "III", "IV"]
    name = "BROKEN-NAME"
    logger.debug(f"Naming {x},{y}")
    if y <= 4:
        name = quadrants[x - 1]
    else:
        name = quadrants[x + 8 - 1]
    if not quadrant_only:
        name += " " + subquadrants[(y - 1) % 4]

    return name


class ShipDevice:
    _damage = 0
    _name = "GenericShipDevice"
    _shortname = "GSD"

    def __repr__(self):
        return f"<{type(self)} Damage: {self.damage}>"

    def damaged(self):
        return self.damage > 0

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        logger.debug(f"{self._name} damage changed - {self._damage} to {value}")
        if self._damage > 0 and value == 0:
            print(f"{self._name} is REPAIRED!")
        if self._damage == 0 and value > 0:
            print(f"{self._name} is DAMAGED!")
        self._damage = value

    def repair(self, amount):
        if self.damage < amount:
            amount = amount - self.damage
            self.damage = 0
            logger.debug(f"REPAIRING {self._name} - there was {amount} energy left over")
            return amount
        else:
            logger.debug(f"REPAIRING {self._name} - it still has {self.damage} damage")
            self.damage -= amount
            return 0


class WarpEngines(ShipDevice):
    _name = "WARP ENGINES"
    _shortname = "NAV"


class ShortRangeSensor(ShipDevice):
    _name = "SHORT RANGE SENSORS"
    _shortname = "SRS"


class LongRangeSensor(ShipDevice):
    _name = "LONG RANGE SENSORS"
    _shortname = "LRS"


class PhaserControl(ShipDevice):
    _name = "PHASER CONTROL"
    _shortname = "PHA"


class PhotonTubes(ShipDevice):
    _name = "PHOTON TUBES"
    _shortname = "TOR"


class DamageControl(ShipDevice):
    _name = "DAMAGE CONTROL"
    _shortname = "DAM"


class ShieldControl(ShipDevice):
    _name = "SHIELD CONTROL"
    _shortcode = "COM"
    _shortname = "SHE"


class LibraryComputer(ShipDevice):
    _name = "LIBRARY COMPUTER"
    _shortcode = "COM"


class Klingon:
    pos = [0, 0]
    energy = 0

    def __init__(self, pos):
        self.pos = pos
        self.energy = 200 * (random.random() + 0.5)


def starbase_count():
    r = random.randint(0, 100)
    if r > 96:
        return 1
    return 0


def klingon_count():
    r = random.randint(0, 100)
    if r > 98:
        return 3
    if r > 95:
        return 2
    if r > 80:
        return 1
    return 0


class QuadrantMap:
    cells = None
    klingons = []
    stars = []
    starbases = []
    # tiles = {
    #     MapObjects.Blank: " ",
    #     MapObjects.StarBase: emoji.emojize(":house:", use_aliases=True),
    #     MapObjects.Star: emoji.emojize(":star:", use_aliases=True),
    #     MapObjects.Enterprise: emoji.emojize(":rocket:", use_aliases=True),
    #     MapObjects.Klingon: emoji.emojize(":space_invader:", use_aliases=True),
    # }
    tiles = {
        MapObjects.Blank: "   ",
        MapObjects.StarBase: "<*>",
        MapObjects.Star: " * ",
        MapObjects.Enterprise: ">!<",
        MapObjects.Klingon: "+K+",
    }

    def __init__(self, n_stars, n_klingons, n_starbases):
        self.cells = [MapObjects.Blank for x in range(64)]
        self.klingons = []
        self.starbases = []
        self.stars = []
        logger.debug(f"Seeding quadrant with {n_klingons} klingons")
        for k in range(n_klingons):
            p = self.position_item_randomly(MapObjects.Klingon)
            pos = [p // 8, p % 8]
            self.klingons.append(Klingon(pos))

        for k in range(n_starbases):
            p = self.position_item_randomly(MapObjects.StarBase)
            self.starbases.append(p)

        for k in range(n_stars):
            p = self.position_item_randomly(MapObjects.Star)
            self.stars.append(p)

        print(self.klingons)

    def __str__(self):
        return f"<{type(self)} {len(self.klingons)}K {len(self.starbases)}SB {len(self.stars)}ST>"

    def position_item_randomly(self, item):
        c = self.find_random_blank()
        self.cells[c] = item

        return c

    def find_random_blank(self):
        while True:
            c = random.randint(0, 63)
            if self.cells[c] == MapObjects.Blank:
                return c

    def draw_shortrange(self):
        print("    " + "   ".join([f" {x} " for x in range(1, 9)]))
        print("  " + "-" * 49)
        for i, row in enumerate(chunks(self.cells, 8), start=1):
            print(f"{i} | " + " | ".join([self.tiles[cell] for cell in row]) + " |")
            print("  " + "-" * 49)

    def _count_items(self, item):
        return sum([1 for x in self.cells if x == item])

    def num_klingons(self):
        return self._count_items(MapObjects.Klingon)

    def num_starbases(self):
        return self._count_items(MapObjects.StarBase)


@dataclass
class QuadrantSummary:
    map: QuadrantMap
    name: str
    klingons: int = 0
    starbases: int = 0
    stars: int = 0
    visited: bool = False


class GalaxyMap:
    map = None

    def __init__(self):
        klingons = [klingon_count() for x in range(64)]
        starbases = [starbase_count() for x in range(64)]
        stars = [random.randint(1, 8) for x in range(64)]
        names = [quadrant_name((1 + x // 8, 1 + x % 8)) for x in range(64)]
        self.map = [QuadrantSummary(map=QuadrantMap(x[2], x[0], x[1]), name=x[3], klingons=x[0], starbases=x[1],
                                    stars=x[2], visited=False) for x in zip(klingons, starbases, stars, names)]

        # print(self.map)

    def draw_longrange(self):
        cells = [f"{c.klingons}{c.starbases}{c.stars}" for c in self.map]
        print("    " + "   ".join([f" {x} " for x in range(1, 9)]))
        print("  " + "-" * 49)
        for i, row in enumerate(chunks(cells, 8), start=1):
            print(f"{i} | " + " | ".join(row) + " |")
            print("  " + "-" * 49)

    def num_klingons(self):
        return sum([m.klingons for m in self.map])

    def num_starbases(self):
        return sum([m.starbases for m in self.map])

    def get_quadrant(self, pos):
        logger.debug(f"Getting quadrant {pos}")
        return self.map[pos[0] + pos[1] * 8]


class Ship:
    devices = []
    quadrant_position = [0, 0]
    galaxy_position = [0, 0]
    energy = 0
    shields = 0
    alert = "GREEN"
    torpedoes = 0

    def __init__(self):
        self.devices = [
            WarpEngines(),
            ShortRangeSensor(),
            LongRangeSensor(),
            PhaserControl(),
            PhotonTubes(),
            DamageControl(),
            ShieldControl(),
            LibraryComputer()
        ]
        self.galaxy_position = (random.randint(0, 7), random.randint(0, 7))

    def warp(self, x, y):
        self.galaxy_position = (x, y)
        # TODO - find a spare spot in the quadrant

    def location_name(self):
        return quadrant_name(self.galaxy_position)


class GameState:
    galaxy = None
    ship = None
    stardate = 0
    start_stardate = 0
    end_stardate = 0

    def __init__(self):
        self.ship = Ship()
        self.galaxy = GalaxyMap()
        self.stardate = random.randint(20, 40) * 100
        self.start_stardate = self.stardate
        self.end_stardate = random.randint(0, 10) + 25 + self.stardate

        # self.galaxy.draw_longrange()
        # q = self.galaxy.get_quadrant(1, 1)
        # q.map.draw_shortrange()

    def initial_briefing(self):
        t9 = self.end_stardate - self.stardate
        x0_str = " IS " if self.galaxy.num_starbases() == 1 else " ARE "
        x_str = "" if self.galaxy.num_starbases() == 1 else "S"
        print(f"YOUR ORDERS ARE AS FOLLOWS:\n")
        print(f"   DESTROY THE {self.galaxy.num_klingons()} KLINGON WARSHIPS WHICH HAVE INVADED")
        print(f"   THE GALAXY BEFORE THEY CAN ATTACK FEDERATION HEADQUARTERS")
        print(f"   ON STARDATE {self.end_stardate}. THIS GIVES YOU {t9} DAYS. THERE{x0_str}"
              f"{self.galaxy.num_starbases()} ")
        print(f"   STARBASE{x_str} IN THE GALAXY FOR RESUPPLYING YOUR SHIP\n\n")

    def all_klingons(self):
        for q in self.galaxy.map:
            if len(q.map.klingons) > 0:
                for k in q.map.klingons:
                    print(f"{q.name} {k.pos} ({k.energy})")

    def new_turn(self):
        quadrant = self.galaxy.get_quadrant(self.ship.galaxy_position)

        if self.stardate == self.start_stardate:
            print("YOUR MISSION BEGINS WITH YOUR STARSHIP LOCATED")
            print(f"IN THE GALACTIC QUADRANT, '{quadrant.name}'.")
        else:
            print(f"NOW ENTERING '{quadrant.name}' QUADRANT . . .")

        if quadrant.klingons > 0:
            print("COMBAT AREA    CONDITION RED")
            if self.ship.shields <= 200:
                print("SHIELDS DANGEROUSLY LOW")


def main():
    print("")
    print("                                    ,------*------,")
    print("                    ,-------------   '---  ------'")
    print("                     '-------- --'      / /")
    print("                         ,---' '-------/ /--,")
    print("                          '----------------'")
    print("")
    print("                    THE USS ENTERPRISE --- NCC-1701")
    print("")

    state = GameState()

    state.initial_briefing()
    state.new_turn()


if __name__ == "__main__":
    main()
