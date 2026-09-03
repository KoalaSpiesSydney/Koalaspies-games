# -*- coding: utf-8 -*-
"""The hazard and safety signs, drawn as inline SVG.

Shapes and colours follow the real thing, because that is the part a
student has to recognise on a bottle or a wall:

  red diamond   GHS hazard pictogram   (white field, black symbol)
  blue circle   you MUST do this       (white symbol)
  red circle    you must NOT do this   (black symbol, red bar)
  green square  safe condition / where to go
  red square    fire equipment
"""

def diamond(inner):
    return ('<svg viewBox="0 0 100 100" role="img">'
            '<polygon points="50,4 96,50 50,96 4,50" fill="#fff" stroke="#d81324" stroke-width="8"'
            ' stroke-linejoin="round"/>'
            '<g fill="#111">' + inner + '</g></svg>')

def blue(inner):
    return ('<svg viewBox="0 0 100 100" role="img">'
            '<circle cx="50" cy="50" r="46" fill="#0b5fa5"/>'
            '<g fill="#fff">' + inner + '</g></svg>')

def prohibit(inner):
    return ('<svg viewBox="0 0 100 100" role="img">'
            '<circle cx="50" cy="50" r="46" fill="#fff" stroke="#d81324" stroke-width="10"/>'
            '<g fill="#111">' + inner + '</g>'
            '<rect x="44" y="-2" width="12" height="104" fill="#d81324"'
            ' transform="rotate(45 50 50)"/></svg>')

def green(inner):
    return ('<svg viewBox="0 0 100 100" role="img">'
            '<rect x="3" y="3" width="94" height="94" rx="8" fill="#0f7a3d"/>'
            '<g fill="#fff">' + inner + '</g></svg>')

def redbox(inner):
    return ('<svg viewBox="0 0 100 100" role="img">'
            '<rect x="3" y="3" width="94" height="94" rx="8" fill="#c1121f"/>'
            '<g fill="#fff">' + inner + '</g></svg>')

FLAME = ('<path d="M52 24c1 9 6 13 9 18 4 6 3 14-2 19a16 16 0 0 1-23-3c-4-6-3-13 1-18'
         ' 2 3 4 5 6 6 1-9-2-15 9-22z"/>')
GROUND = '<rect x="26" y="72" width="48" height="6" rx="3"/>'

SIGNS = [
  # ---- GHS hazard pictograms -------------------------------------------
  ("flammable", diamond(FLAME.replace('M52 24','M52 20') + GROUND),
   "Catches fire easily — keep away from sparks",
   "red diamond with a flame above a line"),

  ("oxidiser", diamond(
      '<circle cx="50" cy="64" r="15" fill="none" stroke="#111" stroke-width="6"/>'
      '<path d="M51 20c1 7 5 10 7 14 3 5 2 11-2 14a12 12 0 0 1-17-2c-3-5-2-10 1-14'
      ' 1 2 3 4 4 5 1-7-1-11 7-17z"/>' + GROUND.replace('y="72"','y="84"').replace('height="6"','height="5"')),
   "Feeds a fire — makes other things burn fiercely",
   "red diamond with a flame over a circle"),

  ("explosive", diamond(
      '<path d="M50 22l5 15 11-9-3 15 15-4-10 11 14 6-14 4 8 12-14-6-1 15-8-12-9 11'
      ' 1-14-15 4 11-11-14-6 15-4-6-14 14 6z"/>'
      '<circle cx="24" cy="26" r="3"/><circle cx="78" cy="24" r="3"/>'
      '<circle cx="22" cy="76" r="3"/>'),
   "May explode if it is heated or knocked",
   "red diamond with an exploding bomb"),

  ("gas", diamond(
      '<g transform="rotate(-20 50 56)">'
      '<rect x="41" y="30" width="19" height="46" rx="9"/>'
      '<rect x="45" y="22" width="11" height="10" rx="2"/>'
      '<rect x="41" y="44" width="19" height="4" fill="#fff"/>'
      '</g>'),
   "Gas stored under pressure — the cylinder may burst",
   "red diamond with a gas cylinder"),

  ("corrosive", diamond(
      # left: liquid eating into a flat surface
      '<g transform="rotate(-38 30 34)"><rect x="25" y="20" width="10" height="20" rx="2"/>'
      '<rect x="25" y="38" width="10" height="4"/></g>'
      '<rect x="31" y="46" width="4" height="9" rx="2"/>'
      '<path d="M18 60h30v8H18z"/>'
      '<path d="M28 60l5 8 5-8z" fill="#fff"/>'
      # right: liquid eating into a hand
      '<g transform="rotate(38 70 34)"><rect x="65" y="20" width="10" height="20" rx="2"/>'
      '<rect x="65" y="38" width="10" height="4"/></g>'
      '<rect x="66" y="46" width="4" height="8" rx="2"/>'
      '<path d="M52 74c0-9 5-15 13-15h11c5 0 8 3 8 7 0 5-4 8-9 8H63z"/>'
      '<path d="M64 59l4 7 5-7z" fill="#fff"/>'),
   "Burns skin and eats through metal",
   "red diamond with liquid burning a hand and a surface"),

  ("toxic", diamond(
      '<path d="M50 24c-12 0-21 9-21 20 0 7 3 11 7 14v7h28v-7c4-3 7-7 7-14 0-11-9-20-21-20z"/>'
      '<circle cx="42" cy="45" r="5" fill="#fff"/><circle cx="58" cy="45" r="5" fill="#fff"/>'
      '<rect x="46" y="54" width="8" height="6" rx="2" fill="#fff"/>'
      '<g transform="rotate(20 50 76)"><rect x="22" y="72" width="56" height="8" rx="4"/></g>'
      '<g transform="rotate(-20 50 76)"><rect x="22" y="72" width="56" height="8" rx="4"/></g>'),
   "Poison — can kill if swallowed or breathed in",
   "red diamond with a skull and crossbones"),

  ("irritant", diamond(
      '<path d="M44 24h12l-2 34H46z"/><circle cx="50" cy="68" r="6"/>'),
   "Irritates skin and eyes; harmful in large amounts",
   "red diamond with an exclamation mark"),

  ("health", diamond(
      '<circle cx="50" cy="36" r="10"/>'
      '<path d="M30 76V62c0-8 9-13 20-13s20 5 20 13v14z"/>'
      '<path d="M50.0 50.5L51.8 57.8L58.1 53.9L54.2 60.2L61.5 62.0L54.2 63.8L58.1 70.1L51.8 66.2L50.0 73.5L48.2 66.2L41.9 70.1L45.8 63.8L38.5 62.0L45.8 60.2L41.9 53.9L48.2 57.8Z" '
      ' fill="#fff"/>'),
   "Long-term harm — may cause cancer or organ damage",
   "red diamond with a starburst on a person's chest"),

  ("environment", diamond(
      '<rect x="16" y="54" width="68" height="4" rx="2"/>'
      '<path d="M22 70c7-11 23-11 30 0-7 11-23 11-30 0z"/>'
      '<path d="M52 62l11-8v32z"/>'
      '<path d="M30 66l7 7m0-7l-7 7" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
      '<rect x="65" y="28" width="6" height="26" rx="2"/>'
      '<path d="M68 40 55 27M68 34l11-11M68 46l9-8" stroke="#111" stroke-width="4.5"'
      ' fill="none" stroke-linecap="round"/>'),
   "Poisons fish and pollutes waterways",
   "red diamond with a dead fish and a bare tree"),

  # ---- must do ----------------------------------------------------------
  ("goggles", blue(
      '<path d="M22 44c0-7 6-12 14-12h28c8 0 14 5 14 12v8c0 7-6 12-14 12h-8l-6-6-6 6h-8'
      'c-8 0-14-5-14-12z"/>'
      '<rect x="14" y="40" width="10" height="6" rx="3"/><rect x="76" y="40" width="10" height="6" rx="3"/>'),
   "You must wear safety glasses here",
   "blue circle with a pair of safety goggles"),

  ("gloves", blue(
      '<path d="M36 40c0-3 2-5 4-5s4 2 4 5v6h2V30c0-3 2-5 4-5s4 2 4 5v16h2V34c0-3 2-5 4-5'
      's4 2 4 5v12h2v-6c0-3 2-5 4-5s4 2 4 5v20c0 9-7 16-17 16h-6c-10 0-15-7-15-16z"/>'
      '<rect x="33" y="74" width="36" height="9" rx="3"/>'
      '<rect x="33" y="71" width="36" height="3" fill="#0b5fa5"/>'),
   "You must wear gloves here",
   "blue circle with a glove"),

  ("labcoat", blue(
      '<path d="M38 22 50 32l12-10 14 9-4 20-6-2v33H34V49l-6 2-4-20z"/>'
      '<path d="M50 34 40 24l-4 3 10 34z" fill="#0b5fa5"/>'
      '<path d="M50 34l10-10 4 3-10 34z" fill="#0b5fa5"/>'
      '<rect x="48" y="60" width="4" height="12" fill="#0b5fa5"/>'),
   "You must wear a lab coat or apron",
   "blue circle with a lab coat"),

  ("noflame", prohibit(FLAME + GROUND),
   "No open flames — do not light anything here",
   "red crossed-out circle over a flame"),

  # ---- where things are -------------------------------------------------
  ("firstaid", green(
      '<rect x="42" y="20" width="16" height="60" rx="3"/>'
      '<rect x="20" y="42" width="60" height="16" rx="3"/>'),
   "The first aid kit is kept here",
   "green square with a white cross"),

  ("shower", green(
      '<rect x="46" y="10" width="6" height="12"/>'
      '<path d="M28 24h44c0 6-10 10-22 10s-22-4-22-10z"/>'
      '<path d="M34 36v10m10-10v12m12-12v12m10-12v10" stroke="#fff" stroke-width="4"/>'
      '<circle cx="50" cy="58" r="7"/>'
      '<path d="M38 90c0-10 5-20 12-20s12 10 12 20z"/>'),
   "Emergency shower — stand under it and pull",
   "green square with a person under a shower"),

  ("eyewash", green(
      '<path d="M22 56c8-12 20-18 28-18s20 6 28 18c-8 12-20 18-28 18s-20-6-28-18z"/>'
      '<circle cx="50" cy="56" r="9" fill="#0f7a3d"/>'
      '<path d="M34 30v12m16-18v14m16-8v12" stroke="#fff" stroke-width="5"/>'),
   "Rinse your eyes here after a splash",
   "green square with an eye and two jets of water"),

  ("extinguisher", redbox(
      '<rect x="38" y="30" width="24" height="52" rx="8"/>'
      '<rect x="44" y="20" width="12" height="12" rx="3"/>'
      '<rect x="56" y="22" width="18" height="5" rx="2"/>'
      '<path d="M72 24l10-8v14z"/>'),
   "A fire extinguisher is kept here",
   "red square with a fire extinguisher"),
]

SIGN_GROUPS = [
  ["flammable", "oxidiser", "noflame"],
  ["corrosive", "irritant"],
  ["toxic", "health"],
  ["goggles", "gloves", "labcoat"],
  ["firstaid", "shower", "eyewash"],
]
