"""Builds the chemistry matching games from one shared template.

Each game is a list of items:  (key, top line, big line, line under, clue, read-aloud)
The key only has to be unique; AVOID_TOGETHER groups refer to it.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.dirname(HERE)          # the games sit one level up, beside index.html
sys.path.insert(0, HERE)
from signs import SIGNS, SIGN_GROUPS

TPL = open(os.path.join(HERE, 'chem_template.html'), encoding='utf-8').read()
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def f(formula):
    """H2SO4 -> H₂SO₄  (digits after a letter or bracket become subscripts)"""
    return re.sub(r'(?<=[A-Za-z)\]])(\d+)', lambda m: m.group(1).translate(SUB), formula)


# ══════════════════════════════════════════════════════════════════════
# GAME 0 — what is it used for  →  the element
# ══════════════════════════════════════════════════════════════════════
USES = [
    (1, "H",   "Hydrogen",    "Rocket fuel and making fertiliser"),
    (2, "He",  "Helium",      "Party balloons and MRI magnets"),
    (3, "Li",  "Lithium",     "Batteries in phones and electric cars"),
    (4, "Be",  "Beryllium",   "X-ray windows and aerospace parts"),
    (5, "B",   "Boron",       "Heat-proof glass and washing powder"),
    (6, "C",   "Carbon",      "Pencils, diamonds and all living things"),
    (7, "N",   "Nitrogen",    "Fertiliser and freezing food"),
    (8, "O",   "Oxygen",      "Breathing masks and making steel"),
    (9, "F",   "Fluorine",    "Toothpaste and non-stick pans"),
    (10, "Ne",  "Neon",        "Glowing shop signs"),
    (11, "Na",  "Sodium",      "Table salt and orange street lamps"),
    (12, "Mg",  "Magnesium",   "Light alloys and bright flares"),
    (13, "Al",  "Aluminium",   "Cans, foil and aeroplanes"),
    (14, "Si",  "Silicon",     "Computer chips and glass"),
    (15, "P",   "Phosphorus",  "Match heads and fertiliser"),
    (16, "S",   "Sulfur",      "Fertiliser and hardening rubber"),
    (17, "Cl",  "Chlorine",    "Disinfecting pools and drinking water"),
    (18, "Ar",  "Argon",       "Shielding welds and filling light bulbs"),
    (19, "K",   "Potassium",   "Fertiliser and soap"),
    (20, "Ca",  "Calcium",     "Bones, teeth and cement"),
    (22, "Ti",  "Titanium",    "Hip joints and jet engines"),
    (23, "V",   "Vanadium",    "Tough tool steel and springs"),
    (24, "Cr",  "Chromium",    "Shiny plating and stainless steel"),
    (25, "Mn",  "Manganese",   "Toughening steel and colouring glass"),
    (26, "Fe",  "Iron",        "Steel for buildings and cars"),
    (27, "Co",  "Cobalt",      "Blue pigment and battery electrodes"),
    (28, "Ni",  "Nickel",      "Coins and stainless steel"),
    (29, "Cu",  "Copper",      "Electrical wiring and water pipes"),
    (30, "Zn",  "Zinc",        "Galvanising steel against rust"),
    (31, "Ga",  "Gallium",     "LEDs and phone chips"),
    (32, "Ge",  "Germanium",   "Fibre optics and infrared lenses"),
    (33, "As",  "Arsenic",     "Semiconductors and old rat poisons"),
    (34, "Se",  "Selenium",    "Photocopiers and anti-dandruff shampoo"),
    (35, "Br",  "Bromine",     "Flame retardants and photographic film"),
    (36, "Kr",  "Krypton",     "Bright lights and camera flashes"),
    (37, "Rb",  "Rubidium",    "Atomic clocks"),
    (38, "Sr",  "Strontium",   "Red fireworks"),
    (40, "Zr",  "Zirconium",   "Nuclear fuel cladding and fake diamonds"),
    (42, "Mo",  "Molybdenum",  "High-strength steel and lubricants"),
    (43, "Tc",  "Technetium",  "Bone and heart scans"),
    (45, "Rh",  "Rhodium",     "Catalytic converters in cars"),
    (46, "Pd",  "Palladium",   "Phone circuits and dental alloys"),
    (47, "Ag",  "Silver",      "Jewellery, mirrors and antibacterials"),
    (48, "Cd",  "Cadmium",     "Yellow paint pigment and old batteries"),
    (49, "In",  "Indium",      "Touchscreens"),
    (50, "Sn",  "Tin",         "Solder and coating steel cans"),
    (52, "Te",  "Tellurium",   "Solar panels and alloys"),
    (53, "I",   "Iodine",      "Antiseptic and iodised salt"),
    (54, "Xe",  "Xenon",       "Car headlights and ion engines"),
    (55, "Cs",  "Caesium",     "The atomic clocks that set world time"),
    (56, "Ba",  "Barium",      "Barium meals for X-rays"),
    (60, "Nd",  "Neodymium",   "Powerful magnets in headphones"),
    (64, "Gd",  "Gadolinium",  "MRI contrast dye"),
    (74, "W",   "Tungsten",    "Light bulb filaments and drill tips"),
    (78, "Pt",  "Platinum",    "Jewellery and catalytic converters"),
    (79, "Au",  "Gold",        "Jewellery and electrical contacts"),
    (80, "Hg",  "Mercury",     "Old thermometers and fluorescent lamps"),
    (82, "Pb",  "Lead",        "Car batteries and radiation shielding"),
    (92, "U",   "Uranium",     "Fuel for nuclear power stations"),
    (95, "Am",  "Americium",   "Smoke detectors"),
]
USES_GROUPS = [
    ["Rh", "Pd", "Pt"],
    ["Ag", "Au", "Pt"],
    ["Li", "Cd", "Co", "Pb"],
    ["Ne", "Kr", "Xe", "Ar"],
    ["Rb", "Cs"],
    ["He", "Gd"],
    ["N", "P", "K", "S"],
    ["Fe", "Mn", "V", "Mo", "Cr", "Ni"],
    ["Si", "Ga", "As", "In"],
    ["U", "Zr"],
    ["Be", "Ba"],
    ["Na", "Cl"],
]

# ══════════════════════════════════════════════════════════════════════
# GAME 1 — everyday name  →  formula and chemical name
# ══════════════════════════════════════════════════════════════════════
COMMON = [
    ("NaCl",        "Sodium chloride",       "Table salt, on every table"),
    ("H2O",         "Water",                 "Rain, rivers and what we drink"),
    ("NaHCO3",      "Sodium bicarbonate",    "Baking soda, raises cakes"),
    ("CaCO3",       "Calcium carbonate",     "Chalk, limestone and seashells"),
    ("CH3COOH",     "Acetic acid",           "Vinegar on your chips"),
    ("C12H22O11",   "Sucrose",               "Table sugar"),
    ("NaOCl",       "Sodium hypochlorite",   "Household bleach"),
    ("H2SO4",       "Sulfuric acid",         "Car battery acid"),
    ("NH3",         "Ammonia",               "Sharp-smelling window cleaner"),
    ("CO2",         "Carbon dioxide",        "The fizz in drinks"),
    ("Fe2O3",       "Iron(III) oxide",       "Rust on an old gate"),
    ("SiO2",        "Silicon dioxide",       "Beach sand and quartz"),
    ("MgSO4",       "Magnesium sulfate",     "Epsom salts for a sore back"),
    ("N2O",         "Nitrous oxide",         "Laughing gas at the dentist"),
    ("C2H5OH",      "Ethanol",               "The alcohol in wine and beer"),
    ("C3H8O",       "Isopropyl alcohol",     "Rubbing alcohol in cleaning wipes"),
    ("H2O2",        "Hydrogen peroxide",     "Antiseptic and hair bleach"),
    ("CaSO4",       "Calcium sulfate",       "Plaster of Paris and plasterboard"),
    ("NaOH",        "Sodium hydroxide",      "Caustic soda, unblocks drains"),
    ("CH4",         "Methane",               "Natural gas in the stove"),
    ("C3H8",        "Propane",               "Bottled gas for the barbecue"),
    ("C4H10",       "Butane",                "Cigarette lighter fuel"),
    ("O3",          "Ozone",                 "The layer that blocks UV"),
    ("NaF",         "Sodium fluoride",       "Added to toothpaste"),
    ("KNO3",        "Potassium nitrate",     "Saltpetre, in gunpowder"),
    ("CaO",         "Calcium oxide",         "Quicklime, burnt from limestone"),
    ("Ca(OH)2",     "Calcium hydroxide",     "Slaked lime and whitewash"),
    ("HCl",         "Hydrochloric acid",     "The acid in your stomach"),
    ("C6H12O6",     "Glucose",               "Blood sugar and sports drinks"),
    ("CO",          "Carbon monoxide",       "Silent killer from faulty heaters"),
    ("SO2",         "Sulfur dioxide",        "Smell of a struck match"),
    ("NH4NO3",      "Ammonium nitrate",      "Fertiliser that can explode"),
    ("Na2CO3",      "Sodium carbonate",      "Washing soda, softens water"),
    ("AgNO3",       "Silver nitrate",        "Stains skin black; old photography"),
    ("TiO2",        "Titanium dioxide",      "White pigment in paint and sunscreen"),
    ("ZnO",         "Zinc oxide",            "White paste on a lifeguard's nose"),
    ("C8H10N4O2",   "Caffeine",              "Keeps you awake in coffee"),
    ("C9H8O4",      "Acetylsalicylic acid",  "Aspirin for a headache"),
    ("KCl",         "Potassium chloride",    "Low-sodium 'lite' salt"),
    ("CuSO4",       "Copper(II) sulfate",    "Blue crystals, kills pool algae"),
]
COMMON_GROUPS = [
    ["CaO", "Ca(OH)2", "CaCO3", "CaSO4"],      # the lime family
    ["NaCl", "KCl"],                            # salts
    ["NaOCl", "H2O2"],                          # bleaches
    ["TiO2", "ZnO"],                            # white pigments
    ["NaHCO3", "Na2CO3", "NaOH"],               # the sodas
    ["CH4", "C3H8", "C4H10"],                   # bottled fuels
    ["C12H22O11", "C6H12O6"],                   # sugars
    ["C2H5OH", "C3H8O"],                        # alcohols
    ["NH4NO3", "KNO3"],                         # fertiliser and gunpowder
    ["CO2", "CO"],                              # one oxygen apart
    ["H2SO4", "HCl"],                           # strong acids
]

# ══════════════════════════════════════════════════════════════════════
# GAME 2 — what is inside it  →  the formula
#   The counts are written out by hand here. build() parses each formula
#   independently and refuses to build if the two disagree, so a typo in
#   either column is caught rather than taught.
# ══════════════════════════════════════════════════════════════════════
COUNTS = [
    ("H2O",       "Water",              [("hydrogen",2), ("oxygen",1)]),
    ("CO2",       "Carbon dioxide",     [("carbon",1), ("oxygen",2)]),
    ("NaCl",      "Sodium chloride",    [("sodium",1), ("chlorine",1)]),
    ("H2SO4",     "Sulfuric acid",      [("hydrogen",2), ("sulfur",1), ("oxygen",4)]),
    ("NH3",       "Ammonia",            [("nitrogen",1), ("hydrogen",3)]),
    ("CH4",       "Methane",            [("carbon",1), ("hydrogen",4)]),
    ("C2H6",      "Ethane",             [("carbon",2), ("hydrogen",6)]),
    ("C3H8",      "Propane",            [("carbon",3), ("hydrogen",8)]),
    ("HNO3",      "Nitric acid",        [("hydrogen",1), ("nitrogen",1), ("oxygen",3)]),
    ("NaOH",      "Sodium hydroxide",   [("sodium",1), ("oxygen",1), ("hydrogen",1)]),
    ("Ca(OH)2",   "Calcium hydroxide",  [("calcium",1), ("oxygen",2), ("hydrogen",2)]),
    ("Mg(NO3)2",  "Magnesium nitrate",  [("magnesium",1), ("nitrogen",2), ("oxygen",6)]),
    ("Al2(SO4)3", "Aluminium sulfate",  [("aluminium",2), ("sulfur",3), ("oxygen",12)]),
    ("(NH4)2SO4", "Ammonium sulfate",   [("nitrogen",2), ("hydrogen",8), ("sulfur",1), ("oxygen",4)]),
    ("CaCO3",     "Calcium carbonate",  [("calcium",1), ("carbon",1), ("oxygen",3)]),
    ("NaHCO3",    "Sodium bicarbonate", [("sodium",1), ("hydrogen",1), ("carbon",1), ("oxygen",3)]),
    ("C6H12O6",   "Glucose",            [("carbon",6), ("hydrogen",12), ("oxygen",6)]),
    ("C12H22O11", "Sucrose",            [("carbon",12), ("hydrogen",22), ("oxygen",11)]),
    ("Fe2O3",     "Iron(III) oxide",    [("iron",2), ("oxygen",3)]),
    ("Fe3O4",     "Magnetite",          [("iron",3), ("oxygen",4)]),
    ("Al2O3",     "Aluminium oxide",    [("aluminium",2), ("oxygen",3)]),
    ("SO2",       "Sulfur dioxide",     [("sulfur",1), ("oxygen",2)]),
    ("SO3",       "Sulfur trioxide",    [("sulfur",1), ("oxygen",3)]),
    ("NO2",       "Nitrogen dioxide",   [("nitrogen",1), ("oxygen",2)]),
    ("N2O",       "Nitrous oxide",      [("nitrogen",2), ("oxygen",1)]),
    ("P4O10",     "Phosphorus pentoxide", [("phosphorus",4), ("oxygen",10)]),
    ("KMnO4",     "Potassium permanganate", [("potassium",1), ("manganese",1), ("oxygen",4)]),
    ("K2Cr2O7",   "Potassium dichromate", [("potassium",2), ("chromium",2), ("oxygen",7)]),
    ("CuSO4",     "Copper(II) sulfate", [("copper",1), ("sulfur",1), ("oxygen",4)]),
    ("ZnCl2",     "Zinc chloride",      [("zinc",1), ("chlorine",2)]),
    ("AgNO3",     "Silver nitrate",     [("silver",1), ("nitrogen",1), ("oxygen",3)]),
    ("H2O2",      "Hydrogen peroxide",  [("hydrogen",2), ("oxygen",2)]),
    ("C2H5OH",    "Ethanol",            [("carbon",2), ("hydrogen",6), ("oxygen",1)]),
    ("CH3COOH",   "Acetic acid",        [("carbon",2), ("hydrogen",4), ("oxygen",2)]),
    ("NH4NO3",    "Ammonium nitrate",   [("nitrogen",2), ("hydrogen",4), ("oxygen",3)]),
    ("Na2CO3",    "Sodium carbonate",   [("sodium",2), ("carbon",1), ("oxygen",3)]),
    ("MgSO4",     "Magnesium sulfate",  [("magnesium",1), ("sulfur",1), ("oxygen",4)]),
    ("CaCl2",     "Calcium chloride",   [("calcium",1), ("chlorine",2)]),
]
COUNTS_GROUPS = [
    ["SO2", "SO3"], ["NO2", "N2O"], ["Fe2O3", "Fe3O4"],
    ["C6H12O6", "C12H22O11"], ["CaCO3", "Na2CO3", "NaHCO3"],
    ["H2O", "H2O2"], ["CH4", "C2H6", "C3H8"],
    ["MgSO4", "CuSO4", "Al2(SO4)3", "(NH4)2SO4", "H2SO4"],
    ["NaCl", "ZnCl2", "CaCl2"], ["HNO3", "AgNO3", "NH4NO3", "Mg(NO3)2"],
    ["NaOH", "Ca(OH)2"],
]

SYMBOL_OF = {
    "hydrogen":"H", "helium":"He", "carbon":"C", "nitrogen":"N", "oxygen":"O",
    "sodium":"Na", "magnesium":"Mg", "aluminium":"Al", "silicon":"Si",
    "phosphorus":"P", "sulfur":"S", "chlorine":"Cl", "potassium":"K",
    "calcium":"Ca", "chromium":"Cr", "manganese":"Mn", "iron":"Fe",
    "copper":"Cu", "zinc":"Zn", "silver":"Ag",
}


def parse_formula(formula):
    """Count the atoms in a formula, brackets included."""
    tokens = re.findall(r'[A-Z][a-z]?|\d+|\(|\)', formula)
    stack, counts, i = [], {}, 0

    def add(target, sym, n):
        target[sym] = target.get(sym, 0) + n

    while i < len(tokens):
        t = tokens[i]
        if t == '(':
            stack.append(counts); counts = {}
        elif t == ')':
            mult = 1
            if i + 1 < len(tokens) and tokens[i+1].isdigit():
                mult = int(tokens[i+1]); i += 1
            inner, counts = counts, stack.pop()
            for sym, n in inner.items():
                add(counts, sym, n * mult)
        elif t.isdigit():
            raise ValueError("stray digit in " + formula)
        else:
            n = 1
            if i + 1 < len(tokens) and tokens[i+1].isdigit():
                n = int(tokens[i+1]); i += 1
            add(counts, t, n)
        i += 1
    if stack:
        raise ValueError("unclosed bracket in " + formula)
    return counts


def check_counts():
    problems = []
    for formula, name, parts in COUNTS:
        stated = {}
        for word, n in parts:
            if word not in SYMBOL_OF:
                problems.append("%s: no symbol known for '%s'" % (formula, word)); continue
            stated[SYMBOL_OF[word]] = stated.get(SYMBOL_OF[word], 0) + n
        actual = parse_formula(formula)
        if stated != actual:
            problems.append("%s (%s): written %s, formula says %s" % (formula, name, stated, actual))
    return problems


# ══════════════════════════════════════════════════════════════════════
# GAME 3 — where it comes from  →  the element
# ══════════════════════════════════════════════════════════════════════
ORES = [
    (13, "Al", "Aluminium",  "Mined as bauxite"),
    (26, "Fe", "Iron",       "Smelted from haematite ore"),
    (82, "Pb", "Lead",       "Mined as galena"),
    (80, "Hg", "Mercury",    "Roasted out of cinnabar"),
    (29, "Cu", "Copper",     "Smelted from chalcopyrite"),
    (30, "Zn", "Zinc",       "Roasted from zinc blende"),
    (50, "Sn", "Tin",        "Mined as cassiterite"),
    (22, "Ti", "Titanium",   "Made from ilmenite and rutile"),
    (74, "W",  "Tungsten",   "Mined as wolframite"),
    (24, "Cr", "Chromium",   "Mined as chromite"),
    (25, "Mn", "Manganese",  "Mined as pyrolusite"),
    (28, "Ni", "Nickel",     "Mined as pentlandite"),
    (56, "Ba", "Barium",     "Mined as barite"),
    (9,  "F",  "Fluorine",   "Mined as fluorite"),
    (15, "P",  "Phosphorus", "Mined as phosphate rock"),
    (19, "K",  "Potassium",  "Mined as potash"),
    (5,  "B",  "Boron",      "Borax from dry lake beds"),
    (92, "U",  "Uranium",    "Mined as pitchblende"),
    (11, "Na", "Sodium",     "Split out of rock salt"),
    (17, "Cl", "Chlorine",   "Split from salt water by electricity"),
    (12, "Mg", "Magnesium",  "Extracted from seawater"),
    (3,  "Li", "Lithium",    "Pumped from salt lake brines"),
    (35, "Br", "Bromine",    "Taken from brines and the Dead Sea"),
    (53, "I",  "Iodine",     "Extracted from seaweed and brines"),
    (7,  "N",  "Nitrogen",   "Chilled out of the air"),
    (8,  "O",  "Oxygen",     "Distilled from liquid air"),
    (18, "Ar", "Argon",      "A by-product of liquid air"),
    (2,  "He", "Helium",     "Trapped in natural gas wells"),
    (6,  "C",  "Carbon",     "Mined as coal and graphite"),
    (14, "Si", "Silicon",    "Made from quartz sand"),
    (20, "Ca", "Calcium",    "Burnt out of limestone"),
    (16, "S",  "Sulfur",     "Recovered when oil is refined"),
    (47, "Ag", "Silver",     "A by-product of lead and copper mining"),
    (79, "Au", "Gold",       "Panned from rivers, crushed from quartz"),
    (78, "Pt", "Platinum",   "Mined with nickel ores in South Africa"),
    (1,  "H",  "Hydrogen",   "Made from natural gas and steam"),
]
ORES_GROUPS = [
    ["N", "O", "Ar", "He"],          # out of the air
    ["Na", "Cl"],                     # out of salt
    ["Li", "Br", "I"],                # out of brines
    ["Ag", "Au", "Pt"],               # precious
    ["Fe", "Cu", "Pb", "Zn", "Ni"],   # smelted and roasted ores
]

# ══════════════════════════════════════════════════════════════════════
# GAME 5 — the reaction  →  what it makes
# ══════════════════════════════════════════════════════════════════════
REACTIONS = [
    ("rust",      "Fe2O3",     "Rust (iron oxide)",       "iron + oxygen →"),
    ("water",     "H2O",       "Water",                   "hydrogen + oxygen →"),
    ("co2",       "CO2",       "Carbon dioxide",          "carbon + oxygen →"),
    ("salt",      "NaCl",      "Salt (sodium chloride)",  "sodium + chlorine →"),
    ("mgo",       "MgO",       "Magnesium oxide",         "magnesium + oxygen → (bright white flame)"),
    ("cuo",       "CuO",       "Copper(II) oxide",        "copper + oxygen → (black coating)"),
    ("so2",       "SO2",       "Sulfur dioxide",          "sulfur + oxygen →"),
    ("nh3",       "NH3",       "Ammonia",                 "nitrogen + hydrogen → (Haber process)"),
    ("hcl_g",     "HCl",       "Hydrogen chloride",       "hydrogen + chlorine →"),
    ("cao_co2",   "CaO + CO2", "Quicklime + carbon dioxide", "limestone, strongly heated →"),
    ("caoh2",     "Ca(OH)2",   "Slaked lime",             "quicklime + water →"),
    ("h2co3",     "H2CO3",     "Carbonic acid",           "carbon dioxide + water →"),
    ("zn_acid",   "ZnCl2 + H2", "Zinc chloride + hydrogen", "zinc + hydrochloric acid →"),
    ("neutralise","NaCl + H2O", "Salt + water",           "hydrochloric acid + sodium hydroxide →"),
    ("burn_ch4",  "CO2 + H2O", "Carbon dioxide + water",  "methane + oxygen → (burning gas)"),
    ("respire",   "CO2 + H2O", "Carbon dioxide + water",  "glucose + oxygen → (respiration)"),
    ("photo",     "C6H12O6 + O2", "Glucose + oxygen",     "carbon dioxide + water → (photosynthesis)"),
    ("h2so4",     "H2SO4",     "Sulfuric acid",           "sulfur trioxide + water →"),
    ("hno3",      "HNO3",      "Nitric acid",             "nitrogen dioxide + water + oxygen →"),
    ("nacl_h2o",  "NaOH + H2 + Cl2", "Caustic soda, hydrogen and chlorine", "salt water + electricity →"),
    ("agcl",      "AgCl",      "Silver chloride (white solid)", "silver nitrate + salt →"),
    ("caco3_ppt", "CaCO3",     "Chalk (the milky bit in limewater)", "limewater + carbon dioxide →"),
    ("baking",    "CO2 + H2O", "Carbon dioxide + water",  "baking soda + vinegar → (the volcano)"),
    ("thermite",  "Al2O3 + Fe", "Aluminium oxide + molten iron", "aluminium + iron oxide → (thermite)"),
]
REACTIONS_GROUPS = [
    ["burn_ch4", "respire", "baking", "h2co3"],   # all end in CO2 and water
    ["cao_co2", "caoh2", "caco3_ppt"],            # the limestone cycle
    ["water", "hcl_g", "salt"],                   # element + element
]


# ══════════════════════════════════════════════════════════════════════
def js(s):
    return json.dumps(s, ensure_ascii=False)


def emit(items, groups):
    rows = ",\n".join(
        "  [%s, %s, %s, %s, %s, %s]" % tuple(js(str(x)) for x in it) for it in items)
    grp = ",\n".join("  [%s]" % ", ".join(js(g) for g in group) for group in groups)
    return rows, grp


def build(filename, title, h1, intro, about, items_about, items, groups,
          plural, nudge_clue, nudge_answer, main_size="1.35em", drawing=False,
          svg_width="min(58%, 4.4em)"):
    rows, grp = emit(items, groups)
    html = (TPL.replace("__ITEMS__", rows)
               .replace("__GROUPS__", grp)
               .replace("__TITLE__", title)
               .replace("__H1__", h1)
               .replace("__INTRO__", intro)
               .replace("__ABOUT__", about)
               .replace("__ITEMS_ABOUT__", items_about)
               .replace("__PLURAL__", plural)
               .replace("__NUDGE_CLUE__", nudge_clue)
               .replace("__NUDGE_ANSWER__", nudge_answer)
               .replace("__MAIN_SIZE__", main_size)
               .replace("__MAIN_IS_DRAWING__", "true" if drawing else "false")
               .replace("min(58%, 4.4em)", svg_width))
    left = re.findall(r'__[A-Z_]+__', html)
    assert not left, "unfilled placeholders: %s" % set(left)
    open(os.path.join(OUT, filename), 'w', encoding='utf-8').write(html)
    print("%-34s %3d items" % (filename, len(items)))


def main():
    problems = check_counts()
    if problems:
        print("ATOM COUNT PROBLEMS:"); [print("  " + p) for p in problems]; sys.exit(1)
    print("atom counts: all %d formulas agree with their written-out contents" % len(COUNTS))

    build("element-uses.html",
          "What Is It Used For? – Periodic Table Matching Game",
          "What Is It Used For? – Periodic Table Matching Game",
          "Turn over a card to read what something is used for, then choose the element that does that job. "
          "Every round deals six new elements, so play again for a fresh set.",
          "Turn over a card to read what an element is used for — and choose\n"
          "   the element that does that job.",
          "Sixty elements a student is likely to meet",
          [(sym, str(z), sym, name, use, name + ", symbol " + sym)
           for z, sym, name, use in USES],
          USES_GROUPS, "elements",
          "Turn over a card first to see what it is used for.",
          "Now choose the element that does that job.",
          main_size="2.2em")

    build("chem-common-names.html",
          "Everyday Names & Formulas – Chemistry Matching Game",
          "Everyday Names &amp; Formulas – Chemistry Matching Game",
          "Turn over a card to read where you would meet a substance, then choose its formula. "
          "Every round deals six new substances, so play again for a fresh set.",
          "Turn over a card to read the everyday name of a substance — baking\n"
          "   soda, bleach, rust — and choose the formula and chemical name that\n"
          "   go with it.",
          "Forty substances a student meets outside the lab",
          [(k, "", f(k), name, clue, "") for k, name, clue in COMMON],
          COMMON_GROUPS, "substances",
          "Turn over a card first to see the everyday name.",
          "Now choose the formula that matches.")

    build("chem-atom-counts.html",
          "What Is Inside It? – Formula Matching Game",
          "What Is Inside It? – Formula Matching Game",
          "Turn over a card to read what a substance is made of, then choose the formula that says so. "
          "Every round deals six new formulas, so play again for a fresh set.",
          "Turn over a card listing the atoms in a substance and choose the\n"
          "   formula that says the same thing. The brackets are the point:\n"
          "   Ca(OH)₂ is one calcium, TWO oxygen and TWO hydrogen.",
          "Thirty-eight formulas, brackets and all",
          [(k, "", f(k), name,
            " · ".join("%d %s" % (n, w) for w, n in parts), "")
           for k, name, parts in COUNTS],
          COUNTS_GROUPS, "formulas",
          "Turn over a card first to see what is inside.",
          "Now choose the formula that matches.")

    build("chem-ores.html",
          "Where Does It Come From? – Periodic Table Matching Game",
          "Where Does It Come From? – Periodic Table Matching Game",
          "Turn over a card to read where something is dug up or drawn from, then choose the element it gives. "
          "Every round deals six new elements, so play again for a fresh set.",
          "Turn over a card describing where a material comes from — an ore, a\n"
          "   brine, the air itself — and choose the element that comes out of it.",
          "Thirty-six elements and where we get them",
          [(sym, str(z), sym, name, clue, name + ", symbol " + sym)
           for z, sym, name, clue in ORES],
          ORES_GROUPS, "elements",
          "Turn over a card first to see where it comes from.",
          "Now choose the element it gives.",
          main_size="2.2em")

    build("chem-reactions.html",
          "What Does It Make? – Word Equation Matching Game",
          "What Does It Make? – Word Equation Matching Game",
          "Turn over a card to read the left-hand side of a reaction, then choose what it makes. "
          "Every round deals six new reactions, so play again for a fresh set.",
          "Turn over a card showing what goes into a reaction and choose what\n"
          "   comes out of it.",
          "Twenty-four reactions a class is likely to meet",
          [(k, "", f(prod), name, clue, "") for k, prod, name, clue in REACTIONS],
          REACTIONS_GROUPS, "reactions",
          "Turn over a card first to see what goes in.",
          "Now choose what the reaction makes.",
          main_size="1.25em")

    build("chem-hazard-signs.html",
          "Hazard & Safety Signs – Laboratory Matching Game",
          "Hazard &amp; Safety Signs – Laboratory Matching Game",
          "Turn over a card to read a warning or an instruction, then choose the sign that means it. "
          "Every round deals six new signs, so play again for a fresh set.",
          "Turn over a card to read what a sign means and choose the sign\n"
          "   itself. The shape and the colour carry half the meaning: a red\n"
          "   diamond warns about the chemical, a blue circle tells you what you\n"
          "   MUST wear, a red circle tells you what you must NOT do, and a green\n"
          "   square tells you where to go if something goes wrong.",
          "Nine GHS hazard pictograms and eight workplace signs",
          [(key, "", svg, "", clue, alt) for key, svg, clue, alt in SIGNS],
          SIGN_GROUPS, "signs",
          "Turn over a card first to read what it means.",
          "Now choose the sign that means it.",
          drawing=True, svg_width="min(88%, 6.6em)")


if __name__ == "__main__":
    main()
