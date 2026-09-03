# Koalaspies · Chemistry Matching Games

Seven free browser games for revising the periodic table and basic chemistry.
No build step, no framework, no tracking — every game is one self-contained
HTML file that runs by double-clicking it.

© Modern English Australia · Sydney. All rights reserved.

---

## Publishing it

1. Create a repository on GitHub and push this folder to it.
2. **Settings → Pages → Source: Deploy from a branch**, branch `main`, folder `/ (root)`.
3. Wait a minute. The site appears at `https://<your-username>.github.io/<repo-name>/`.

That is the whole setup. The files are flat and every link between them is
relative, so the site works the same on GitHub Pages, in Moodle, on a memory
stick, or opened straight off the desktop.

`.nojekyll` is there to stop GitHub running the files through Jekyll. Leave it.

---

## What is in here

| File | The question it asks | Cards |
|---|---|---|
| `index.html` | the hub page — every game embedded in an iframe | |
| `element-symbols.html` | which element does this symbol stand for? | 118 |
| `element-uses.html` | what do we use this element for? | 60 |
| `chem-ores.html` | where does this element come from? | 36 |
| `chem-common-names.html` | what is this everyday substance really called? | 40 |
| `chem-atom-counts.html` | what is inside this formula? | 38 |
| `chem-reactions.html` | what does this reaction make? | 24 |
| `chem-hazard-signs.html` | what does this safety sign mean? | 17 |

### The QR code

Every page — the hub and all seven games — has a QR code in the top left
corner. Tap it and it fills the screen, which is the size you need for it to
scan from the back of a room.

There is nothing to configure. The code is generated at runtime from
`location.href`, so it always points at wherever the page is actually open:
your GitHub Pages URL once it is live, your Moodle URL if you upload it there,
and a `file://` path if you are testing it off the desktop.

### How the games play

Six pairs are dealt each round — twelve cards, four across and three down.

Turn over a face-down card to read the clue, then choose the answer it belongs
to. Until a clue is showing, the answer cards are dashed and out of play; once
one is showing, the *other* clue cards go out of play. That way only one clue
is ever readable and a student cannot flip through all six to read the answers
before committing. A wrong guess costs nothing and puts the board back to the
start of the step.

No verb, element or formula comes up twice until the whole list has been
played, and the counter under the title tracks how much of the list a class
has covered.

`element-symbols.html` is the original game and still plays the other way
round — choose a symbol first, then find its name.

---

## Screens it has been checked on

Every page was tested at 320 × 568 (iPhone SE), 390 × 844, 844 × 390 (a phone
turned sideways), 768 × 1024 and 1024 × 768 (iPad both ways), 1280 × 800 and
1920 × 1080. On each: nothing scrolls sideways, no card clips its text, the QR
stays clear of the brand line, the whole board and the Play Again button stay
on screen, and the button stays at least 44px — the size a thumb needs.

A phone held sideways gets its own layout: stacked, the board and the button
cannot both fit in 390px of height, so the title, progress line and button move
to the left and the board takes the right half.

The `svh` units that size the board have a `vh` fallback for older browsers.

---

## Editing a game

Open the file in any text editor and look for the block marked
`TO EDIT THE LIST`. Each line is one card:

```js
["id", "small line", "big line", "line under", "the clue", "read aloud as"]
```

The `id` only has to be unique. Leave `""` for any line you do not want. Keep
the clue to about six words — it has to fit inside a square card.

Below the list is `AVOID_TOGETHER`: sets of items that are never dealt into
the same round. This matters more than it looks. Rhodium and platinum both end
up in a catalytic converter; caesium and rubidium both run atomic clocks; four
different elements go into fertiliser. Deal two of those together and both
cards are arguably right, which makes a correct game feel broken. Add a line
whenever you add items whose clues overlap.

To change how many pairs are dealt, set `PAIRS_PER_ROUND` to `8` for a 4 × 4
board of sixteen cards.

---

## Rebuilding in bulk (optional)

`source/` holds the Python that generated six of the seven games from one
template (`element-symbols.html` is your original and is not generated).
You do **not** need it to edit or publish anything — it is only useful for
changing something across several games at once.

```
source/chem_template.html   the shared page: layout, rules of play, styling
source/chem_build.py        the word lists, and the build itself
source/signs.py             the hazard and safety signs, drawn as SVG
python3 source/chem_build.py
```

The atom counts in `chem_build.py` are written out by hand *and* parsed
independently from each formula at build time, brackets included. If the two
ever disagree the build stops rather than shipping a wrong card.

---

## Credits

Games and content by Modern English Australia, Sydney.
QR codes are generated at runtime by [goqr.me](https://goqr.me/api/) from
whatever URL the page is open at, so they point at your site once it is live —
there is nothing to configure.
