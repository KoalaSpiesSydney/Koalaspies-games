# Koalaspies — Japanese Kanji & Hiragana Matching Games

Twelve free browser games. Ten cover the first **800 kanji** in the order Japanese schools
teach them; the last two give practice on **160 compound words** built from characters in
those levels. No build step, no dependencies, no server code — plain HTML, CSS and JavaScript.

Each game holds 80 items and asks one thing: the character (or word), and how it is read in
hiragana. Choose one, then turn over cards to find its reading. Six new items per round.

---

## The twelve games

| Level | Kanji | Source | Band |
|---|---|---|---|
| 1 | 80 | School Grade 1 | Beginner |
| 2 | 80 | School Grade 2 (1st half) | Beginner |
| 3 | 80 | School Grade 2 (2nd half) | Beginner |
| 4 | 80 | School Grade 3 (1–80) | Elementary |
| 5 | 80 | School Grade 3 (81–160) | Elementary |
| 6 | 80 | Grade 3 (161–200) + Grade 4 (1–40) | Elementary |
| 7 | 80 | School Grade 4 (41–120) | Intermediate |
| 8 | 80 | School Grade 4 (121–200) | Intermediate |
| 9 | 80 | Grade 4 (201–202) + Grade 5 (1–78) | Intermediate |
| 10 | 80 | School Grade 5 (79–158) | Upper intermediate |
| 11 | 80 words | Compounds from Levels 1–6 | Word practice |
| 12 | 80 words | Compounds from Levels 1–10 | Word practice |

**Levels 11 and 12 are word practice.** Instead of single characters, every card is a real
two-kanji compound — 学校, 病院, 政治, 責任 — and the student has to read the whole word. This
is a different skill from character recognition: you can only read 図書 if you know both 図
and 書 *and* which reading each takes in combination.

Level 11 draws mostly on Levels 1–6 (everyday vocabulary: school, family, travel, health).
Level 12 draws mostly on Levels 9–10 (abstract vocabulary: economy, law, evidence, argument).
Between them the 160 words use 259 of the 800 characters — the ones that actually form common
compounds. Place-name kanji such as 埼, 潟 and 阜 do not appear, because they rarely form
ordinary words.

**Every character in all 160 words is taught somewhere in Levels 1–10.** The build script
refuses to generate these two files if even one word uses a kanji outside the 800, so a
student can never meet a character the games have not covered.

Grade boundaries do not fall on multiples of 80 (the grades hold 80 / 160 / 200 / 202 / 193
characters), so Levels 6 and 9 straddle a boundary. Every other level sits inside one grade.

Roughly 650 kanji is the JLPT N3 / intermediate threshold, so a student who finishes
Level 9 is there, and Level 10 is already past it.

---

## Publishing to GitHub Pages

1. Push this folder to a new repository.
2. **Settings → Pages → Source: Deploy from a branch**, branch `main`, folder `/ (root)`.
3. The site appears at `https://<username>.github.io/<repo>/` within a minute or two.

`index.html` is at the root and every link is relative, so it works from any sub-path.
The `.nojekyll` file stops GitHub's Jekyll build from touching the files.

Locally, just open `index.html` — every game is self-contained, so it works from disk too.

---

## What's in here

```
index.html            Landing page — all twelve games embedded
.nojekyll             Tells GitHub Pages to skip Jekyll processing
levels.json           Manifest: level number, grade, band, blurb, sample kanji

kanji-level-1.html    Level 1    80 kanji
kanji-level-2.html    Level 2    80 kanji
...
kanji-level-10.html   Level 10   80 kanji
kanji-level-11.html   Level 11   80 compound words   (word practice)
kanji-level-12.html   Level 12   80 compound words   (word practice)
```

Each game file is completely self-contained — its kanji data, styling and logic are all
inside it. Delete one and only its own card on the landing page stops working.

`index.html` is generated from `levels.json`, so if you edit a blurb or a band there,
regenerate rather than hand-editing both.

---

## QR codes

Every game carries a QR code in its top-left corner encoding **that game's own URL**, so a
student who scans Level 7's code lands on Level 7. It reads `location.href` at runtime and
picks up your real domain automatically once published — nothing to configure.

Tapping the code enlarges it, which is the point: a 38-pixel square will not scan from the
back of a classroom.

The images come from `api.qrserver.com`. That is the only external request the games make,
apart from Google Fonts on the landing page.

---

## Spoken readings

Turn over a reading card and the game says it aloud. This uses the browser's built-in
speech synthesis (`speechSynthesis`), so there are no audio files to host and every one of
the 960 readings can be spoken — including any you add later.

- **Only reading cards speak.** Voicing the kanji card would hand over the answer before
  the student has read it.
- **A toggle sits in the top-right corner**, mirroring the QR code on the left. Sound is on
  by default; tapping it mutes.
- **No Japanese voice, no sound.** If the device has no `ja-JP` voice the toggle hides
  itself and nothing is spoken — reading kana aloud in an English accent is worse than
  silence, and with the button hidden there would be no way to switch it off.
- Speech is read at 0.85× rate, a little slower than default, which is easier to follow.

Voice availability varies: iOS, macOS, Windows and Android almost always have a Japanese
voice; some Linux browsers have none. Nothing about the game depends on it — the games work
exactly the same with sound unavailable.

Because speech is only ever triggered by a tap, browser autoplay restrictions never apply.

---

## Editing the kanji

The data sits near the bottom of each game file:

```js
const ELEMENTS = [
  ["一","いち","one"],["右","みぎ","right"], ...
];
```

Format: `[kanji, reading in hiragana, English meaning]`.

Levels 11 and 12 use exactly the same shape, with a word in the first slot:

```js
["学校","がっこう","school"],["病院","びょういん","hospital"], ...
```

If you add a word there, make sure both its characters appear in Levels 1–10 — that is the
whole point of these two games, and `build_words.py` enforces it.

Readings include okurigana where that is how the character is actually read — 見 is `みる`,
高 is `たかい`. Kun'yomi where a common one exists, on'yomi otherwise.

### Homophones are handled for you

Japanese has a lot of same-reading characters — Level 9 alone has 制, 性 and 政 all reading
`せい`. If two of them landed in the same round, both tiles would be correct and picking
either would look like a bug.

`dealRound()` prevents this: it refuses to place two identical readings in one round and
pushes the clash back into the queue for a later round. **You do not need to keep readings
unique** — add or edit entries freely.

There are 26 such pairs across the ten levels. They are listed by the build script, not
stored in the files, because the engine handles them at runtime.

### Round size

Near the top of each game's script:

```js
const PAIRS_PER_ROUND = 6;   // 6 pairs = 12 cards = a 4×3 board
```

Change to 8 for a 4×4 board of 16 cards.

---

## Kanji sources

School-grade (kyōiku) assignments are the official MEXT list: 80 / 160 / 200 / 202 / 193 /
191 characters for grades 1–6, 1,026 in total. Levels 1–10 cover grades 1 through most of
grade 5.

Readings and meanings are one representative reading per character — the one a learner is
most likely to meet first — not a full dictionary entry.

---

## What comes next

Levels 13 onward would be the last 35 of Grade 5, then Grade 6's 191 characters, which would
complete the full kyōiku set of 1,026 in about three more games. More word games could follow
the same pattern — the only rule is that every character must already be taught.

---

## Notes

- An earlier JLPT-ordered series (`kanji-match.html` plus `kanji-set*.js`) was replaced by
  these levels. If those files are still on a server anywhere, they are superseded.
- The compound cards use a smaller face than the single-kanji levels, since two characters
  have to fit the same square.
- The landing page footer links only to pages outside this repo. If you add `contact.html`
  or similar here, add them back to the footer.
