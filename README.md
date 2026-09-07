# Ashmere — concept site

A Grade I house, 2,400 acres, and a hundred-year plan. Eleven pages, no build
step required to view, no dependencies, no framework.

## Open it

Unzip the whole folder first, then open `index.html`.
`index.html` on its own will render unstyled — the stylesheet, script, fonts and
video all live in the sibling `assets/` folder.

To serve it locally instead:

    python3 -m http.server 8000

then visit http://localhost:8000

## Pages

| file | what it is |
|---|---|
| `index.html` | home, full-bleed meadow video |
| `house.html` | five rooms, 1583 to 1866, and how the fabric is kept |
| `gardens.html` | walled garden, west park, lake, yew walk, arboretum |
| `meadow.html` | the restoration, **the quadrat survey**, and the cut |
| `long-plan.html` | **the hundred-year plan**, 1560 to 2124, interactive |
| `stay.html` | four lettings on the estate |
| `kitchen.html` | the farm, the dairy, the kitchen |
| `occasions.html` | five event spaces with capacities and constraints |
| `journal.html` | index of six pieces |
| `journal-hay.html` | one full long-form article |
| `visit.html` | **the estate year ring**, tickets, travel, FAQ, enquiry |

## Rebuilding the HTML

The eleven pages come from one template so the header, nav and footer cannot
drift apart. `build.py` holds both the template and all the copy.

    cd ashmere
    python3 build.py

It rewrites the eleven `.html` files **in this folder**, beside `assets/`, and
touches nothing inside `assets/`. It has to write here: every path in the pages
is relative, so HTML generated into a subfolder would load no CSS, JS, font or
video. If `assets/` is not next to `build.py` the script stops with an error
rather than producing pages that cannot find their own stylesheet.

## The video

Every clip is derived from one supplied shot of a meadow. The camera in the
source pans steadily at about 30 px/s, which made a crossfade loop double-expose
the oak. Instead the crop window travels with the pan to hold the tree still,
and the loop is a ping-pong — seamless by construction, with no blend at all.

| file | what it is |
|---|---|
| `meadow-1600.mp4` | hero loop, desktop |
| `meadow-1280.mp4` | hero loop, laptop and tablet |
| `meadow-mobile.mp4` | hero loop, purpose-built portrait reframe |
| `dusk-1600.mp4` | cool low-key regrade, used behind the dark page headers |
| `*.webp` | posters and one blurred still |

## Fonts

Self-hosted and subsetted, 69 KB for both. Newsreader carries the display and
the body text, with the optical-size axis pinned at 30 — shipping both axes cost
127 KB against 53 KB. Familjen Grotesk carries labels, counts and controls.

Both are SIL OFL. If you publish this, add the licence text alongside the fonts.

## Opening it straight off disk

Everything works from `file://`. Your console will show two CORS lines per page
about the `.woff2` preloads: a `file://` page has a null origin, so the browser
refuses the *preload*, while `@font-face` still fetches the same files and both
typefaces render. The preload is kept because it saves a round trip when the
site is hosted. Serving over `http://` removes the messages.

## Notes

Ashmere is fictional. The meadow footage is the single asset supplied with the
brief, counter-panned, regraded and reframed for each page.
