#!/usr/bin/env python3
"""Ashmere — static build. One shell, eleven pages, no duplicated chrome."""
import os, re, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
# Pages must land beside assets/, because every href in the shell is relative to
# them. Writing to a subfolder produces HTML that loads no CSS, JS, font or video.
OUT  = ROOT

SITE = dict(name="Ashmere", tel="+44 1608 000 000", mail="estate@ashmere.example",
            place="Welbury valley, Oxfordshire")

# (slug, short label for the bar, full label for the sheet and footer)
NAV = [("house","The House","The House"),("gardens","Gardens","Gardens & Park"),
       ("meadow","The Meadow","The Meadow"),("long-plan","Long Plan","The Long Plan"),
       ("stay","Stay","Stay"),("kitchen","Farm","Farm & Kitchen"),
       ("occasions","Occasions","Occasions"),("journal","Journal","Journal"),
       ("visit","Visit","Visit")]

ROOMS = [
 ("The Stone Hall","1583","The oldest room standing, and the only one that has never been re-floored. The screen at the north end came out of a ship; nobody has ever established which."),
 ("The Long Gallery","1601","Forty-two metres, built for walking in bad weather. The plaster ceiling took a team of six eleven years and they signed it, in a corner, where they thought nobody would look."),
 ("The Library","1748","Nine thousand volumes, of which about four hundred are worth anything and the rest are worth keeping. Open to researchers by arrangement."),
 ("The Garden Room","1812","Added when the family decided the house should face the park rather than the road. It was the right decision and it cost them the drive."),
 ("The Kitchen Court","1866","Still a working kitchen. The range was converted in 1978 and the copper is used, not polished."),
]

AREAS = [
 ("The Walled Garden","1.6 ha","Four quarters, box-edged, worked on a five-year rotation. About seventy per cent of what the kitchen uses in summer comes out of here, and the glasshouse takes it into November."),
 ("The West Park","210 ha","Wood pasture with 340 veteran oaks, the oldest recorded at around 640 years. Grazed by a small herd that keeps the sward open without touching the trees."),
 ("The Lake and Cascade","11 ha","Dug in 1771 and silted almost solid by 1990. Dredged over three winters; the cascade ran again in 2004 for the first time in a lifetime."),
 ("The Yew Walk","—","Planted 1690, and the one thing on the estate we will not alter. It is cut once a year, by hand, over five weeks."),
 ("The Arboretum","24 ha","Started 1908 and still filling. Two hundred and eleven species, labelled, with the failures left in place and labelled too."),
]

STAYS = [
 dict(slug="gardeners",name="The Gardener's House",n="01",sleeps=4,beds=2,rate=210,
   where="In the walled garden",
   copy="Two bedrooms inside the garden wall, which means you are locked in with the vegetables after six when the gate is shut. Warm, thick-walled and very quiet.",
   detail=["Inside the walled garden","Wood burner","Kitchen garden access","Dogs welcome"]),
 dict(slug="lodge",name="East Lodge",n="02",sleeps=2,beds=1,rate=165,
   where="At the park gate",
   copy="A one-bedroom gatehouse at the end of the lime avenue. Small, round, and slightly absurd, which is the point of a lodge.",
   detail=["One bedroom","Log fire","Ten minutes' walk to the house","No parking at the door"]),
 dict(slug="dairy",name="The Old Dairy",n="03",sleeps=6,beds=3,rate=340,
   where="Beside the farmyard",
   copy="Three bedrooms in the converted dairy, with the original slate slabs still down in the hall. Close enough to the farm to be woken by it.",
   detail=["Three bedrooms","Slate floors","Farmyard on the doorstep","Sleeps six"]),
 dict(slug="north-wing",name="The North Wing",n="04",sleeps=8,beds=4,rate=780,
   where="In the house itself",
   copy="Four bedrooms in the house, with your own stair and your own door onto the terrace. Taken whole, and not let while the house is open to visitors.",
   detail=["Inside the main house","Private terrace door","Four bedrooms","Whole-wing only"]),
]

SPACES = [
 ("The Stone Hall","Seated dinner","90","Ceremony 120","No amplified music after 22:00"),
 ("The Long Gallery","Reception","200","Standing only","No fixed heating"),
 ("The Orangery","Seated dinner","140","Dancing 180","Licensed for ceremonies"),
 ("The Tithe Barn","Seated dinner","180","Dancing 250","Marquee not required"),
 ("The Walled Garden","Ceremony","150","Reception 200","Weather-dependent"),
]

PLAN_EVENTS = [
 (1583,"The house is finished","Built on the footings of a grange, using stone from the same quarry that still supplies our repairs."),
 (1690,"The Yew Walk is planted","Two hundred and eight yews. All but four are still standing."),
 (1771,"The lake is dug","Along with the cascade, by a workforce of ninety over two summers."),
 (1782,"The west park oaks go in","Four hundred and ten of them, for timber nobody alive would see cut."),
 (1908,"The arboretum is started","A hedge against losing species we had not yet noticed we were losing."),
 (1947,"The estate is nearly sold","Death duties. Two farms went; the park did not."),
 (1994,"Meadow restoration begins","Green hay from a surviving meadow eight miles away, spread on ploughed ground."),
 (2004,"The cascade runs again","After three winters of dredging."),
 (2011,"The endowment is settled","Sized to cover the roof, the yews and the oaks in perpetuity, not the events diary."),
 (2026,"Where we are now","Two hundred and forty acres under restoration, nine hundred trees planted in the last decade."),
 (2048,"The 1994 meadows reach full richness","On current counts, around thirty-eight species per square metre."),
 (2072,"First thinning of the 2010 oaks","The last people to make a decision about these trees will not have met us."),
 (2124,"The plan horizon","Everything committed today is costed to here. Beyond it is somebody else's problem, deliberately."),
]

JOURNAL = [
 dict(slug="journal-hay",date="4 August",read="8 min",kicker="The Meadow",
   title="Why we cut the meadow exactly once",
   standfirst="A hay meadow is not a lawn that has been left alone. It is a crop with one harvest, and the date of that harvest decides what grows there for the next hundred years.",
   feature=True),
 dict(slug=None,date="19 July",read="5 min",kicker="The House",
   title="The plasterers signed the Long Gallery ceiling",
   standfirst="Six men, eleven years, and a small inscription in the north-west corner that nobody found until 1961."),
 dict(slug=None,date="2 July",read="6 min",kicker="The Long Plan",
   title="What an endowment is actually for",
   standfirst="Ours covers the roof, the yews and the oaks. It does not cover the café, and that is on purpose."),
 dict(slug=None,date="11 June",read="4 min",kicker="The Park",
   title="Counting the veteran oaks",
   standfirst="Three hundred and forty, girthed and photographed. The oldest is somewhere around 640 and we will not say where it is."),
 dict(slug=None,date="26 May",read="7 min",kicker="Farm",
   title="We stopped ploughing the top ground",
   standfirst="Four years of direct drilling, one bad harvest, and a soil carbon figure that finally started moving the right way."),
 dict(slug=None,date="8 May",read="3 min",kicker="Gardens",
   title="The glasshouse is older than the boiler that heats it",
   standfirst="1871 and 1953 respectively, and the argument about replacing either of them is now in its fourth decade."),
]

FAQS = [
 ("When is the house open?","The house opens Wednesday to Sunday from late March to the end of October, 11:00 to 17:00, last entry 16:15. The gardens, park and meadow are open every day of the year from 09:00 until dusk, including when the house is shut."),
 ("Do we need to book?","For the house, yes, in high summer — we cap it at 400 a day so the rooms stay walkable. Gardens and park are never capped and never need booking."),
 ("Can we walk the meadow?","Yes, on the mown paths, all year. Between the middle of May and the cut in late July please keep to them; you are walking through a seed crop, and one boot off the path costs more than it looks like it does."),
 ("Are dogs allowed?","In the park and on the estate walks, on a lead between March and July because of ground-nesting birds. In the gardens, assistance dogs only. In the house, no."),
 ("Is it accessible?","Partly, and we would rather say so plainly. The ground floor of the house, the Orangery, the walled garden and the lakeside path are all step-free. The Long Gallery is up sixteen stairs with no lift, the park paths are grass and rut in winter, and the Yew Walk has a gravel surface. Ring us and we will tell you honestly what will work."),
 ("Can we take photographs?","Anywhere outside, freely. Inside the house, no flash and no tripods. Commercial shoots go through the estate office and we say no more often than yes."),
]

TICKETS = [
 ("House, gardens and park","22.00","11.00","Under 5 free"),
 ("Gardens and park only","12.00","6.00","Under 5 free"),
 ("Meadow and estate walks","Free","Free","Always"),
 ("Annual pass","55.00","27.50","Two named adults"),
]

MONTHS = [
 ("Jan","Park and meadow open. The house is shut and the yews are being cut."),
 ("Feb","Snowdrops through the Yew Walk. Winter pruning in the walled garden."),
 ("Mar","House opens late in the month. Blackthorn along the west park boundary."),
 ("Apr","Cowslips in the meadow. The glasshouse fills up."),
 ("May","Buttercups, and the best fortnight of the year. Paths only from mid-month."),
 ("Jun","Orchids in the south meadow, if it has been wet enough. Roses in the walled garden."),
 ("Jul","Yellow rattle sets seed. The meadow is cut in the last week."),
 ("Aug","Hay lifted, aftermath grazing begins. Fruit in the walled garden."),
 ("Sep","Arboretum starts to turn. Best month for the lake."),
 ("Oct","House closes at the end of the month. Fungi in the west park."),
 ("Nov","Tree planting starts. Park open, everything else winding down."),
 ("Dec","Planting continues. The park on a hard frost is worth the drive."),
]

# ══════════════════════════════════════════════════════════════════════════
def shell(slug, title, desc, body, scripts="", body_class=""):
    nav = "".join('<li><a href="%s.html"%s>%s</a></li>' %
                  (s, ' aria-current="page"' if s == slug else "", short) for s, short, _ in NAV)
    sheet = "".join('<li><a href="%s.html"><span>%s</span></a></li>' % (s, full) for s, _, full in NAV)
    fnav = "".join('<li><a href="%s.html">%s</a></li>' % (s, full) for s, _, full in NAV[:5])
    fnav2 = "".join('<li><a href="%s.html">%s</a></li>' % (s, full) for s, _, full in NAV[5:])
    return f"""<!doctype html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{H.escape(title)} — {SITE['name']}</title>
<meta name="description" content="{H.escape(desc)}">
<meta name="theme-color" content="#EDEFE8">
<meta property="og:title" content="{H.escape(title)} — {SITE['name']}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:type" content="website">
<link rel="preload" href="assets/fonts/newsreader-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/familjen-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
<script>document.documentElement.className="js";</script>
</head>
<body class="{body_class}" data-page="{slug}">
<a class="skip" href="#main">Skip to content</a>

<header class="bar" id="bar">
  <a class="mark" href="index.html" aria-label="{SITE['name']}, home">
    <svg class="mark__g" width="24" height="30" viewBox="0 0 24 30" aria-hidden="true" focusable="false">
      <path d="M12 1.2c3.4 2.6 6.2 3.6 10.2 3.6 0 9.4-1.4 17.6-10.2 23.9C3.2 22.4 1.8 14.2 1.8 4.8 5.8 4.8 8.6 3.8 12 1.2Z"
            fill="none" stroke="currentColor" stroke-width="1.15" stroke-linejoin="round"/>
      <path d="M12 8.4v11M8.4 12.2 12 14.6l3.6-2.4" fill="none" stroke="currentColor"
            stroke-width="1.15" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <span class="mark__w">Ashmere</span>
  </a>
  <nav class="bar__nav" aria-label="Primary"><ul>{nav}</ul></nav>
  <p class="openchip" id="openChip"><span class="openchip__d"></span><span id="openText">Estate open</span></p>
  <a class="btn btn--sm" href="visit.html#plan">Plan a visit</a>
  <button class="burger" id="burger" aria-expanded="false" aria-controls="sheet" aria-label="Open menu">
    <span></span><span></span>
  </button>
</header>

<div class="sheet" id="sheet" hidden>
  <nav aria-label="Mobile"><ul>{sheet}</ul></nav>
  <a class="btn btn--block" href="visit.html#plan">Plan a visit</a>
  <p class="sheet__c">{SITE['tel']}<br>{SITE['mail']}</p>
</div>

<main id="main">
{body}
</main>

<footer class="foot">
  <div class="wrap foot__top">
    <div class="foot__brand">
      <p class="foot__mk">Ashmere</p>
      <p class="foot__tag">A Grade&nbsp;I house, 2,400 acres in the {SITE['place']},<br>
        and a plan that runs to 2124.</p>
      <a class="btn btn--ghost" href="visit.html#plan">Plan a visit</a>
    </div>
    <div class="foot__cols">
      <div><h2>The estate</h2><ul>{fnav}</ul></div>
      <div><h2>More</h2><ul>{fnav2}</ul></div>
      <div><h2>Reach us</h2><ul>
        <li><a href="tel:{SITE['tel'].replace(' ','')}">{SITE['tel']}</a></li>
        <li><a href="mailto:{SITE['mail']}">{SITE['mail']}</a></li>
        <li><span>{SITE['place']}</span></li>
        <li><span>Estate office 09:00 – 17:00</span></li>
      </ul></div>
    </div>
  </div>
  <div class="wrap foot__base">
    <p>© 2026 The Ashmere Estate Trust</p>
    <p class="foot__fine">Concept site. Ashmere is a fictional estate; the meadow footage is
      the single asset supplied with the brief, counter-panned, regraded and reframed for each page.</p>
  </div>
</footer>

<script src="assets/js/site.js" defer></script>{scripts}
</body>
</html>
"""


def phead(kind, eyebrow, title, lede, extra=""):
    media = ""
    if kind == "dusk":
        media = ('<div class="phead__media"><video class="phead__v" muted loop playsinline preload="none" '
                 'data-src="assets/media/dusk-1600.mp4" poster="assets/media/poster-dusk.webp" '
                 'aria-hidden="true" tabindex="-1"></video><div class="phead__scrim"></div></div>')
    elif kind == "haze":
        media = '<div class="phead__media phead__media--haze"></div>'
    return f"""<section class="phead phead--{kind}">
  {media}
  <div class="wrap phead__in">
    <p class="eyebrow reveal">{eyebrow}</p>
    <h1 class="phead__h reveal">{title}</h1>
    <p class="lede reveal">{lede}</p>
    {extra}
  </div>
</section>"""


def build():
    P = {}

    # ══ HOME ══
    P["index"] = shell("index","We plant for people we will never meet",
      "Ashmere is a Grade I house and 2,400 acres in the Welbury valley, run on a hundred-year plan.",
      f"""
<section class="hero">
  <div class="hero__media">
    <video class="hero__v" id="heroVideo" muted loop playsinline autoplay disablepictureinpicture
           preload="none" tabindex="-1"></video>
    <div class="hero__scrim"></div>
  </div>
  <div class="wrap hero__in">
    <h1 class="hero__h">
      <span class="ln"><span>We plant for people</span></span>
      <span class="ln"><span>we will never meet.</span></span>
    </h1>
    <p class="hero__lede">A Grade&nbsp;I house and 2,400 acres in the {SITE['place']}.
      The oaks in the west park went in in 1782. The ones we planted last winter are for 2140.</p>
    <div class="hero__acts">
      <a class="btn" href="visit.html#plan">Plan a visit</a>
      <a class="btn btn--line" href="long-plan.html">See the hundred-year plan</a>
    </div>
  </div>
  <button type="button" class="motion" id="motionBtn" aria-pressed="true" aria-label="Background video">
    <span class="motion__d"></span><span id="motionLabel">Playing</span>
  </button>
</section>

<section class="band">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">The estate</p>
      <h2 class="reveal">Held in trust, worked as a farm, open most days.</h2></div>
    <div class="two__r">
      <p class="lede reveal">Ashmere has been in one family since 1583 and in a charitable trust
        since 2011. The trust owns the house, the park and the endowment that keeps them; the farm
        pays its own way.</p>
      <p class="reveal">There is no theme, no trail and nothing costumed. The house is open five
        days a week in season, the gardens and the meadow are open every day of the year, and the
        best thing here costs nothing and is a field.</p>
      <dl class="facts reveal">
        <div><dt>Acres</dt><dd>2,400</dd></div>
        <div><dt>Veteran oaks</dt><dd>340</dd></div>
        <div><dt>Since</dt><dd>1583</dd></div>
        <div><dt>Plan runs to</dt><dd>2124</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="band band--park">
  <div class="wrap">
    <blockquote class="pull reveal">
      <p>A garden you finish is a garden you have stopped thinking about.</p>
      <footer>— Margaret Ivey, head gardener 1961&ndash;1994</footer>
    </blockquote>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <header class="head">
      <div><p class="eyebrow reveal">What is here</p><h2 class="reveal">Four things, and they are not equal.</h2></div>
      <p class="lede reveal">The house is the reason most people come. The meadow is the reason
        we think the place matters.</p>
    </header>
    <div class="grid4">
      <article class="tile"><a href="house.html"><span class="tile__n">01</span>
        <h3>The House</h3><p>Five rooms open, 1583 to 1866, and a ceiling its makers signed.</p>
        <span class="tile__m">Wed&ndash;Sun in season</span></a></article>
      <article class="tile"><a href="gardens.html"><span class="tile__n">02</span>
        <h3>Gardens &amp; Park</h3><p>A walled garden, 210 hectares of wood pasture and a cascade that runs again.</p>
        <span class="tile__m">Open daily</span></a></article>
      <article class="tile"><a href="meadow.html"><span class="tile__n">03</span>
        <h3>The Meadow</h3><p>Thirty years of restoration, cut once a year, free to walk.</p>
        <span class="tile__m">Open daily, free</span></a></article>
      <article class="tile"><a href="kitchen.html"><span class="tile__n">04</span>
        <h3>Farm &amp; Kitchen</h3><p>1,100 acres in hand, a dairy, and a kitchen that buys from both.</p>
        <span class="tile__m">Shop open daily</span></a></article>
    </div>
  </div>
</section>

<section class="band band--tight">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">The long plan</p>
      <h2 class="reveal">Costed to 2124.</h2></div>
    <div class="two__r">
      <p class="lede reveal">Every commitment we make is priced out to the end of the next
        century — the roof, the yew walk, the oaks, the meadow. Anything we cannot fund that far
        ahead, we do not start.</p>
      <p class="reveal">It sounds grand and it is mostly just arithmetic. It also means nobody
        here is in a hurry, which visitors notice within about ten minutes.</p>
      <p class="more reveal"><a href="long-plan.html">Move through the plan, 1583 to 2124</a></p>
    </div>
  </div>
</section>

<section class="cta">
  <div class="wrap cta__in">
    <h2 class="reveal">Come on a Wednesday.</h2>
    <p class="lede reveal">It is the quietest day the house is open, the gardeners are all out,
      and you will very likely have the Long Gallery to yourself.</p>
    <div class="cta__acts"><a class="btn btn--lg" href="visit.html#plan">Plan a visit</a>
      <a class="btn btn--line btn--lg" href="stay.html">Stay the night</a></div>
  </div>
</section>
""", scripts='\n<script>window.ASH_HERO=1;</script>', body_class="on-hero")

    # ══ HOUSE ══
    rows = "".join(f"""
      <article class="room">
        <div class="room__id"><span class="room__n">{i+1:02d}</span><h2>{r[0]}</h2></div>
        <p class="room__yr">{r[1]}</p>
        <p class="lede">{r[2]}</p>
      </article>""" for i, r in enumerate(ROOMS))
    P["house"] = shell("house","The House",
      "Five rooms open to visitors, from the 1583 Stone Hall to the 1866 kitchen court.",
      phead("dusk","The House","Four hundred years of people not quite finishing it.",
        "Nothing here was built all at once and nothing was ever properly completed. Five rooms "
        "are open; the rest is lived in, worked in, or held up with scaffolding.") + f"""
<section class="band band--tight"><div class="wrap rooms">{rows}</div></section>

<section class="band band--park">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">The collection</p>
      <h2 class="reveal">Mostly ordinary, entirely local.</h2></div>
    <div class="two__r">
      <p class="lede reveal">There is no masterpiece here and we have stopped apologising for it.
        What there is instead is four centuries of one family buying from within about thirty miles.</p>
      <p class="reveal">Nine hundred objects are catalogued and the catalogue is public. The
        furniture is largely Oxfordshire, the portraits are largely bad, and the two things worth
        travelling for are a 1602 estate map and a set of dairy ledgers that runs unbroken from
        1740 to 1961.</p>
      <ul class="ticks reveal">
        <li><b>The 1602 estate map</b> — the earliest surviving survey of the valley, on vellum</li>
        <li><b>The dairy ledgers</b> — 221 unbroken years, digitised in 2019</li>
        <li><b>The Long Gallery ceiling</b> — signed by its plasterers, found 1961</li>
        <li><b>The library</b> — 9,000 volumes, open to researchers by arrangement</li>
      </ul>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <header class="head">
      <div><p class="eyebrow reveal">Keeping it up</p><h2 class="reveal">The roof is the whole argument.</h2></div>
      <p class="lede reveal">Everything else on this estate is negotiable. The roof is what the
        endowment exists for.</p>
    </header>
    <div class="mats">
      <article class="mat"><h3>Stone</h3><p>From the same quarry as the original build, two miles
        south, reopened by the trust in 2013 purely to supply repairs. It is cheaper than matching
        it on the open market and the colour is right.</p></article>
      <article class="mat"><h3>Lead</h3><p>Recast on site every time a section comes off. The
        1583 lead is still up there in places, on its fourth casting.</p></article>
      <article class="mat"><h3>Lime</h3><p>Hot-mixed on the yard. Cement was used on the south
        front in 1958 and we have spent thirty years taking it back off.</p></article>
      <article class="mat"><h3>Oak</h3><p>From the estate, seasoned four years in the timber
        yard. The 1782 planting was made for exactly this and is only now coming to it.</p></article>
    </div>
  </div>
</section>
""")

    # ══ GARDENS ══
    ar = "".join(f"""
      <article class="area">
        <div class="area__h"><h2>{a[0]}</h2><p class="area__m">{a[1]}</p></div>
        <p class="lede">{a[2]}</p>
      </article>""" for a in AREAS)
    P["gardens"] = shell("gardens","Gardens & Park",
      "A walled garden, 210 hectares of wood pasture, a lake and cascade, a 1690 yew walk and an arboretum.",
      phead("light","Gardens & Park","Open every day of the year, including the ones nobody comes.",
        "Two hundred and forty hectares of garden and park. Five gardeners, two foresters and a "
        "grazier. No bedding out, no annual scheme, and nothing that has to be replanted every spring.") + f"""
<section class="band band--tight"><div class="wrap areas">{ar}</div></section>

<section class="band band--park">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">How it is worked</p>
      <h2 class="reveal">Five gardeners, and none of them in a hurry.</h2></div>
    <div class="two__r">
      <p class="lede reveal">A garden this size cannot be kept to a standard. It can only be kept
        to a direction, and the direction here has not changed since Margaret Ivey set it in 1961.</p>
      <p class="reveal">No chemical herbicide anywhere on the estate since 2007. No peat since 2011.
        Compost is made on site from the garden, the stables and the kitchen, and it is the single
        biggest reason the walled garden still produces what it does at this latitude.</p>
      <dl class="facts facts--inv reveal">
        <div><dt>Gardeners</dt><dd>5</dd></div>
        <div><dt>Herbicide-free since</dt><dd>2007</dd></div>
        <div><dt>Peat-free since</dt><dd>2011</dd></div>
        <div><dt>Compost made</dt><dd>310 t/yr</dd></div>
      </dl>
    </div>
  </div>
</section>
""")

    # ══ MEADOW ══
    P["meadow"] = shell("meadow","The Meadow",
      "Thirty years of hay-meadow restoration, surveyed by quadrat, cut once a year in late July.",
      phead("light","The Meadow","The most valuable thing here is a field, and it is free.",
        "Ninety-eight hectares of restored hay meadow, begun in 1994 with green hay from a "
        "surviving meadow eight miles away. It is cut once a year and grazed after, and that is "
        "the entire management.") + """
<section class="band band--park" id="quadrat">
  <div class="wrap">
    <header class="head head--inv">
      <div><p class="eyebrow reveal">Survey</p><h2 class="reveal">Drop a quadrat anywhere.</h2></div>
      <p class="lede reveal">This is how a meadow is actually measured: a one-metre frame, thrown
        or placed, and everything inside it written down. Move ours around the south meadow and
        see what the 2025 survey found.</p>
    </header>
    <div class="quad">
      <figure class="quad__map">
        <svg id="quadSvg" viewBox="0 0 720 500" role="img"
             aria-label="Plan of the south meadow. Move the survey frame to read the species recorded at that point.">
          <defs><linearGradient id="mg" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#2C5330"/><stop offset="100%" stop-color="#1D3D25"/>
          </linearGradient></defs>
          <rect width="720" height="500" fill="url(#mg)"/>
          <g id="quadZones"></g><g id="quadPaths"></g><g id="quadLabels"></g><g id="quadFrame"></g>
        </svg>
        <figcaption class="quad__cap">South meadow, 14 hectares. Darker ground is older
          restoration; the 1994 block is richest because it has had thirty seasons of seed return.</figcaption>
      </figure>
      <div class="quad__panel">
        <div class="quad__read">
          <span class="quad__n" id="quadCount">0</span>
          <span class="quad__u">species in this square metre</span>
        </div>
        <p class="quad__zone" id="quadZone">—</p>
        <ul class="quad__list" id="quadList" aria-live="polite"></ul>
        <div class="quad__ctl">
          <label class="f"><span>Across</span>
            <input id="quadX" type="range" min="60" max="660" step="2" value="300"></label>
          <label class="f"><span>Up</span>
            <input id="quadY" type="range" min="60" max="440" step="2" value="250"></label>
        </div>
        <p class="quad__note">Drag on the map, or use the two controls. Counts are the mean of
          five 2025 quadrats in each block.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">The cut</p>
      <h2 class="reveal">Once, in the last week of July.</h2></div>
    <div class="two__r">
      <p class="lede reveal">Not before, because the yellow rattle has to set and drop. Not after,
        because the sward goes over and the aftermath will not come. One date, and it decides the
        next hundred years.</p>
      <p class="reveal">The hay is lifted within four days and goes to the dairy. Cattle come on
        in the middle of August and stay until the ground turns, treading seed in as they go. Then
        nothing at all until the following July.</p>
      <ol class="steps reveal">
        <li><b>May to July</b><p>Left entirely alone. Paths mown, everything else standing.</p></li>
        <li><b>Last week of July</b><p>Cut, turned twice, baled and lifted inside four days.</p></li>
        <li><b>Mid-August to October</b><p>Aftermath grazing. Roughly one cow to the hectare.</p></li>
        <li><b>November to April</b><p>Nothing. No feeding, no topping, no rolling.</p></li>
      </ol>
    </div>
  </div>
</section>
""", scripts='\n<script>window.ASH_QUAD=1;</script>')

    # ══ LONG PLAN ══
    P["long-plan"] = shell("long-plan","The Long Plan",
      "Ashmere's hundred-year plan: what was planted when, what it becomes, and what is committed to 2124.",
      phead("dusk","The Long Plan","Costed to 2124, which is the point.",
        "Everything the trust commits to is priced to the end of the next century. If we cannot "
        "fund a thing that far ahead, we do not begin it. Drag through five and a half centuries "
        "and watch the estate arrive.") + """
<section class="band band--tight" id="scale">
  <div class="wrap">
    <div class="plan">
      <div class="plan__stage">
        <svg id="planSvg" viewBox="0 56 900 324" role="img"
             aria-label="The estate through time. Trees and buildings appear at the year they were planted or built and mature as the scale advances.">
          <defs>
            <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#DDE4EC"/><stop offset="100%" stop-color="#EDEFE8"/>
            </linearGradient>
          </defs>
          <rect width="900" height="380" fill="url(#skyG)"/>
          <g id="planGround"></g><g id="planTrees"></g><g id="planBuild"></g><g id="planNear"></g><g id="planTags"></g>
        </svg>
      </div>
      <div class="plan__scale">
        <div class="plan__yearrow">
          <span class="plan__year" id="planYear">2026</span>
          <span class="plan__tense" id="planTense">today</span>
        </div>
        <input id="planTime" type="range" min="1560" max="2124" step="1" value="2026"
               aria-label="Year" aria-describedby="planNote">
        <ol class="plan__ticks" id="planTicks"></ol>
      </div>
      <div class="plan__note" id="planNote" aria-live="polite">
        <h2 id="planTitle">Where we are now</h2>
        <p id="planBody">Two hundred and forty acres under restoration, nine hundred trees planted in the last decade.</p>
      </div>
    </div>
  </div>
</section>

<section class="band band--park">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">The endowment</p>
      <h2 class="reveal">It covers the roof, the yews and the oaks. Nothing else.</h2></div>
    <div class="two__r">
      <p class="lede reveal">Settled in 2011 and deliberately narrow. It is sized to keep the
        fabric and the two plantings that cannot be replaced, in perpetuity, at a 2.8 per cent
        real draw.</p>
      <p class="reveal">It does not cover the café, the shop, the events diary or the staff who
        run them. Those pay for themselves or they stop, and one of them has stopped. Keeping the
        endowment narrow is what makes the hundred-year number believable rather than a slogan.</p>
      <dl class="facts facts--inv reveal">
        <div><dt>Real draw</dt><dd>2.8%</dd></div>
        <div><dt>Covers</dt><dd>Fabric only</dd></div>
        <div><dt>Settled</dt><dd>2011</dd></div>
        <div><dt>Horizon</dt><dd>2124</dd></div>
      </dl>
    </div>
  </div>
</section>
""", scripts='\n<script>window.ASH_PLAN=1;</script>')

    # ══ STAY ══
    st = "".join(f"""
    <article class="let" id="{s['slug']}">
      <div class="let__id"><span class="let__n">{s['n']}</span><h2>{s['name']}</h2>
        <p class="let__w">{s['where']}</p></div>
      <div class="let__b"><p class="lede">{s['copy']}</p>
        <ul class="let__f">{''.join('<li>%s</li>' % d for d in s['detail'])}</ul>
        <p class="let__cta"><a class="btn btn--line btn--sm" href="visit.html#plan">Ask about {s['name']}</a></p></div>
      <dl class="let__m">
        <div><dt>Sleeps</dt><dd>{s['sleeps']}</dd></div>
        <div><dt>Bedrooms</dt><dd>{s['beds']}</dd></div>
        <div><dt>From</dt><dd>£{s['rate']} a night</dd></div>
        <div><dt>Minimum</dt><dd>Two nights</dd></div>
      </dl>
    </article>""" for s in STAYS)
    P["stay"] = shell("stay","Stay",
      "Four lettings on the estate, from a one-bedroom gatehouse to four bedrooms in the house itself.",
      phead("haze","Stay","Four places, and the park after everyone has gone.",
        "The best hour here is between six and seven, when the gates shut and the light comes "
        "flat across the west park. Staying is the only way to get it.") + f"""
<section class="band band--tight"><div class="wrap lets">{st}</div></section>

<section class="band band--park">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">In every letting</p>
      <h2 class="reveal">What comes as standard.</h2></div>
    <div class="two__r"><ul class="ticks reveal">
      <li>Free run of the gardens and park outside opening hours</li>
      <li>Breakfast things in, from the farm and the walled garden</li>
      <li>Wood for the fire, cut on the estate and properly seasoned</li>
      <li>No television anywhere; a decent radio in each</li>
      <li>Parking at the estate yard, a short walk from each door</li>
      <li>Two nights minimum, three over bank holidays</li>
    </ul></div>
  </div>
</section>
""")

    # ══ KITCHEN ══
    P["kitchen"] = shell("kitchen","Farm & Kitchen",
      "Eleven hundred acres in hand, a dairy, a walled garden and a kitchen that buys from all three.",
      phead("haze","Farm & Kitchen","The farm pays its own way. That is not a small thing.",
        "Eleven hundred acres in hand, a hundred and forty milkers, and a kitchen two fields from "
        "both. The estate is not subsidised by the visitors and the visitors are not subsidised "
        "by the farm.") + """
<section class="band band--tight">
  <div class="wrap">
    <header class="head">
      <div><p class="eyebrow reveal">The farm</p><h2 class="reveal">Four years off the plough.</h2></div>
      <p class="lede reveal">Direct drilling since 2022, herbal leys in the rotation, and one
        genuinely bad harvest that we are not going to pretend did not happen.</p>
    </header>
    <div class="mats">
      <article class="mat"><h3>Arable</h3><p>620 acres, direct drilled since 2022. Yields dipped
        for two seasons and have come back; soil organic matter is up from 3.1 to 4.0 per cent,
        which is the number that actually matters.</p></article>
      <article class="mat"><h3>The dairy</h3><p>140 cows, block calving in spring, out at grass
        from March to November. Milk goes to a cheesemaker eleven miles away and comes back as
        something we sell in the shop.</p></article>
      <article class="mat"><h3>The walled garden</h3><p>1.6 hectares supplying roughly seventy
        per cent of what the kitchen uses between May and October, and the glasshouse takes salad
        into November.</p></article>
      <article class="mat"><h3>Woodland</h3><p>280 acres, continuous cover, no clear-fell. It
        supplies the estate's own timber and firewood and sells the rest standing.</p></article>
    </div>
  </div>
</section>

<section class="band band--park">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">The kitchen</p>
      <h2 class="reveal">One menu, written at nine, served at noon.</h2></div>
    <div class="two__r">
      <p class="lede reveal">The kitchen in the stable yard does lunch every day the estate is
        open and dinner on Fridays and Saturdays. There is one menu and it is decided by what
        came out of the garden that morning.</p>
      <p class="reveal">Nothing is bought in from further than forty miles except coffee, salt,
        and the things you would rightly think us mad to try to grow here. The bread is made on
        site. So, since 2018, is the butter.</p>
      <dl class="facts facts--inv reveal">
        <div><dt>Lunch</dt><dd>12:00–14:30</dd></div>
        <div><dt>Dinner</dt><dd>Fri &amp; Sat</dd></div>
        <div><dt>Grown here</dt><dd>~70%</dd></div>
        <div><dt>Sourcing radius</dt><dd>40 miles</dd></div>
      </dl>
    </div>
  </div>
</section>
""")

    # ══ OCCASIONS ══
    sp = "".join(f"""<tr><th scope="row">{s[0]}</th><td>{s[1]}</td><td>{s[2]}</td>
      <td>{s[3]}</td><td class="tl">{s[4]}</td></tr>""" for s in SPACES)
    P["occasions"] = shell("occasions","Occasions",
      "Five spaces for weddings and dinners, from 90 seated in the Stone Hall to 250 dancing in the Tithe Barn.",
      phead("light","Occasions","We take about thirty a year, and we turn down more than that.",
        "Weddings, dinners and the occasional company that understands what it is booking. The "
        "estate is not an events venue with a house attached; it is a house that will, carefully, "
        "hold an event.") + f"""
<section class="band band--tight">
  <div class="wrap">
    <div class="tablewrap reveal">
      <table class="rates">
        <caption class="vh">Event spaces, capacities and constraints</caption>
        <thead><tr><th scope="col">Space</th><th scope="col">Best for</th><th scope="col">Seated</th>
          <th scope="col">Also</th><th scope="col" class="tl">Worth knowing</th></tr></thead>
        <tbody>{sp}</tbody>
      </table>
    </div>
    <p class="note reveal">Exclusive use of the house and gardens from £14,000 for a full day.
      The Tithe Barn alone starts at £4,200. Both include the estate team, and neither includes
      catering, which goes through our own kitchen.</p>
  </div>
</section>

<section class="band band--park">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">Before you ask</p>
      <h2 class="reveal">Three things we will not do.</h2></div>
    <div class="two__r"><ul class="ticks reveal">
      <li><b>Fireworks</b> — never. There are 340 veteran oaks and a barn owl population here.</li>
      <li><b>Marquees on the south lawn</b> — the ground is a scheduled archaeological site. The Tithe Barn exists precisely so you do not need one.</li>
      <li><b>Amplified music outdoors after 22:00</b> — the estate is a working farm with neighbours who calve at four in the morning.</li>
      <li><b>Two weddings in a weekend</b> — one at a time, so the gardens get a day to recover.</li>
    </ul></div>
  </div>
</section>
""")

    # ══ JOURNAL ══
    f0 = JOURNAL[0]
    rest = "".join(f"""
      <article class="post reveal">
        <p class="post__m"><span>{p['kicker']}</span><span>{p['date']}</span><span>{p['read']}</span></p>
        <h2>{p['title']}</h2><p>{p['standfirst']}</p>
      </article>""" for p in JOURNAL[1:])
    P["journal"] = shell("journal","Journal",
      "Notes from the estate: the meadow, the house, the farm and the plan.",
      phead("light","Journal","Written by whoever did the thing.",
        "Published when there is something to say. Some of it is about failures, because those "
        "are the entries people actually write to us about.") + f"""
<section class="band band--tight">
  <div class="wrap">
    <a class="feature reveal" href="{f0['slug']}.html">
      <p class="post__m"><span>{f0['kicker']}</span><span>{f0['date']}</span><span>{f0['read']}</span></p>
      <h2>{f0['title']}</h2><p class="lede">{f0['standfirst']}</p>
      <span class="feature__go">Read it</span>
    </a>
    <div class="posts">{rest}</div>
  </div>
</section>
""")

    # ══ ARTICLE ══
    P["journal-hay"] = shell("journal-hay", f0["title"], f0["standfirst"], f"""
<article class="art">
  <header class="wrap art__head">
    <p class="post__m reveal"><span><a href="journal.html">Journal</a></span><span>{f0['kicker']}</span>
      <span>{f0['date']}</span><span>{f0['read']}</span></p>
    <h1 class="reveal">{f0['title']}</h1>
    <p class="lede reveal">{f0['standfirst']}</p>
    <p class="art__by reveal">By Tom Reddish, who drives the mower</p>
  </header>

  <div class="art__fig"><div class="art__figimg"></div>
    <p class="art__cap">The south meadow on 21 July, four days before the cut. The rattle has gone over and the seed is down.</p></div>

  <div class="wrap art__body">
    <p>People assume a wildflower meadow is what happens when you stop mowing. It is very nearly
      the opposite. Stop mowing a field in this country and in fifteen years you have scrub, in
      forty you have woodland, and at no point on the way do you have a meadow. A hay meadow is a
      crop. It exists because somebody takes one cut off it a year, at the same time each year,
      and then puts animals on it.</p>

    <p>We began ours in 1994 with green hay — freshly cut, still-seeding hay carted from a
      surviving meadow eight miles away and spread on ground we had ploughed that autumn. It is
      slow, it is unreliable, and it is still the best method anybody has. Thirty-one years on,
      the 1994 block carries around thirty-four species per square metre. The block we did in
      2016 carries nineteen. The difference is time and nothing else.</p>

    <h2>The date does the work</h2>

    <p>The single most consequential decision on ninety-eight hectares is which week we cut. Cut
      in June and the sward looks immaculate, the hay is superb, and the yellow rattle has not set
      seed — so next year there is less rattle, so the grasses are less suppressed, so there is
      less of everything else, and in six years you have a nice green field with no flowers in it.</p>

    <p>Rattle is the hinge. It is a hemiparasite: it taps the roots of vigorous grasses and takes
      about a third of their vigour away, which is what lets the slower, smaller species get
      light. Everything we do is arranged around letting it seed. That means late July, and it
      means accepting hay that is coarser and lower in feed value than any dairy farmer would
      choose.</p>

    <blockquote><p>Cut a week early and the hay is better and the meadow is worse. That trade is
      the whole job.</p></blockquote>

    <h2>Then the animals</h2>

    <p>Lifting the hay is only half of it. What actually returns seed to the ground is cattle,
      on from the middle of August at about one to the hectare, treading and dunging and opening
      up small patches of bare soil that seed can get into. Sheep will not do it — they graze too
      tight and too selectively, and they leave you a lawn.</p>

    <p>They come off when the ground turns, usually late October. After that nothing happens at
      all until the following July. No feeding, no topping, no rolling, no fertiliser of any
      description. The temptation to intervene over the winter is considerable and it is always
      wrong.</p>

    <h2>What we got wrong</h2>

    <p>Two things. The first is that we spread green hay on three blocks in 1998 without ploughing
      properly first, because it was a wet autumn and we were behind. Those blocks are still the
      worst on the estate and the only fix is to start them again, which we will do in 2028.</p>

    <p>The second is that for the first decade we cut the whole ninety-eight hectares in the same
      week. It is efficient and it is bad practice: it removes every source of nectar on the
      estate on a single day in late July, which for invertebrates is a cliff edge. Since 2009 we
      have left roughly one hectare in eight standing until September, rotating which. It costs
      us about four tonnes of hay a year and it is the cheapest thing we have ever bought.</p>

    <p>The meadow will keep improving for another twenty years or so on current trajectory, and
      then it will hold. Nobody working here now will see the 2016 block reach what the 1994 block
      is at today. That is normal, on this estate, and it is not a complaint.</p>
  </div>

  <div class="wrap art__foot">
    <a class="btn btn--line" href="journal.html">More from the journal</a>
    <a class="btn" href="meadow.html#quadrat">Try the quadrat</a>
  </div>
</article>
""")

    # ══ VISIT ══
    tk = "".join(f"""<tr><th scope="row">{t[0]}</th><td>{'£'+t[1] if t[1][0].isdigit() else t[1]}</td>
      <td>{'£'+t[2] if t[2][0].isdigit() else t[2]}</td><td class="tl">{t[3]}</td></tr>""" for t in TICKETS)
    faq = "".join(f"""
      <div class="faq__i"><h3><button type="button" class="faq__q" aria-expanded="false"
        aria-controls="fa{i}">{q}<span class="faq__x" aria-hidden="true"></span></button></h3>
        <div class="faq__a" id="fa{i}"><div><p>{a}</p></div></div></div>""" for i, (q, a) in enumerate(FAQS))
    P["visit"] = shell("visit","Visit",
      "Opening times, tickets, the estate year month by month, how to get to the Welbury valley, and an enquiry form.",
      phead("dusk","Visit","The gardens are open every day of the year.",
        "The house keeps season hours; everything outdoors does not. Nothing here needs booking "
        "except the house in high summer, and the meadow never costs anything.") + f"""
<section class="band band--tight" id="year">
  <div class="wrap">
    <header class="head">
      <div><p class="eyebrow reveal">The estate year</p><h2 class="reveal">When to come, and what for.</h2></div>
      <p class="lede reveal">Choose a month. May and June are the meadow; September is the lake
        and the arboretum; February is snowdrops and almost nobody else.</p>
    </header>
    <div class="ring">
      <div class="ring__wheel" id="ringWheel"></div>
      <div class="ring__read">
        <p class="ring__m" id="ringMonth">May</p>
        <p class="ring__t" id="ringText">Buttercups, and the best fortnight of the year.</p>
        <p class="ring__hint">Click a month, or use the arrow keys.</p>
      </div>
    </div>
  </div>
</section>

<section class="band" id="plan">
  <div class="wrap">
    <header class="head">
      <div><p class="eyebrow reveal">Tickets</p><h2 class="reveal">Per person, and the field is free.</h2></div>
      <p class="lede reveal">Members of the Trust go free. Everything outdoors is open dawn to
        dusk every day, including Christmas.</p>
    </header>
    <div class="tablewrap reveal">
      <table class="rates">
        <caption class="vh">Admission prices</caption>
        <thead><tr><th scope="col">Admission</th><th scope="col">Adult</th>
          <th scope="col">Child 5&ndash;16</th><th scope="col" class="tl">Notes</th></tr></thead>
        <tbody>{tk}</tbody>
      </table>
    </div>
    <p class="note reveal">House open Wednesday to Sunday, late March to end of October, 11:00 to
      17:00, last entry 16:15. Gardens, park and meadow open daily, 09:00 until dusk.</p>
  </div>
</section>

<section class="band band--tight">
  <div class="wrap two">
    <div class="two__l"><p class="eyebrow reveal">Getting here</p>
      <h2 class="reveal">Twenty minutes off the motorway and then a lane.</h2></div>
    <div class="two__r"><ol class="steps reveal">
      <li><b>By car</b><p>Twenty minutes from the M40, then two miles of single-track lane with
        passing places. Free parking in the meadow field, or on hard standing when it is wet.</p></li>
      <li><b>By train</b><p>Nearest station is eleven minutes away by taxi. There are usually two
        waiting; if there are not, ring the estate office and we will sort something out.</p></li>
      <li><b>On foot</b><p>The valley footpath runs through the park and is open whether we are
        or not. It is four miles from the village and the last mile is the good bit.</p></li>
      <li><b>By bicycle</b><p>Racks at the stable yard. The lane is narrow and fast in places;
        the bridleway from the north is slower and much nicer.</p></li>
    </ol></div>
  </div>
</section>

<section class="band band--tight">
  <div class="wrap">
    <header class="head">
      <div><p class="eyebrow reveal">Questions</p><h2 class="reveal">The ones we are actually asked.</h2></div>
      <p class="lede reveal">Including the two we would rather answer here than in the car park.</p>
    </header>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="band band--park" id="enquire">
  <div class="wrap">
    <header class="head head--inv">
      <div><p class="eyebrow reveal">Write to us</p><h2 class="reveal">A person reads these.</h2></div>
      <p class="lede reveal">The estate office answers within two working days. For a wedding or
        a large group, tell us the date and we will tell you straight away whether it is free.</p>
    </header>
    <form class="form" id="enquiry">
      <div class="form__grid">
        <p class="f"><label for="fName">Your name</label>
          <input id="fName" name="name" type="text" autocomplete="name" required></p>
        <p class="f"><label for="fMail">Email</label>
          <input id="fMail" name="email" type="email" autocomplete="email" required></p>
        <p class="f"><label for="fAbout">What about</label>
          <select id="fAbout" name="about">
            <option>A visit</option><option>Staying on the estate</option>
            <option>A wedding or event</option><option>Research or the archive</option>
            <option>Something else</option></select></p>
        <p class="f"><label for="fWhen">Roughly when</label>
          <input id="fWhen" name="when" type="month"></p>
        <p class="f f--wide"><label for="fMsg">Anything we should know</label>
          <textarea id="fMsg" name="message" rows="4"
            placeholder="Group size, access needs, whether you are bringing a dog — whatever is useful."></textarea></p>
      </div>
      <div class="form__foot">
        <button class="btn btn--lg" type="submit">Send it</button>
        <p class="form__note">We will only use this to answer you. No list, no newsletter.</p>
      </div>
      <noscript><p class="form__note">This form needs JavaScript. Write to
        <a href="mailto:{SITE['mail']}">{SITE['mail']}</a> or ring {SITE['tel']}.</p></noscript>
      <p class="form__ok" id="formOk" role="status" hidden></p>
    </form>
  </div>
</section>
""", scripts='\n<script>window.ASH_VISIT=1;</script>')

    probe = os.path.join(OUT, "assets", "css", "site.css")
    if not os.path.isfile(probe):
        raise SystemExit("build.py could not find assets/ beside itself.\n  expected: %s\n"
                         "Keep build.py in the project root, next to assets/, and run it from there."
                         % probe)
    for slug, doc in P.items():
        open(os.path.join(OUT, slug + ".html"), "w").write(doc)
    print("built %d pages into %s" % (len(P), OUT))
    for slug in sorted(P):
        print("  %-20s %6.1f KB" % (slug + ".html",
              os.path.getsize(os.path.join(OUT, slug + ".html")) / 1024))
    print("open index.html from that folder; assets/ must stay beside it.")


if __name__ == "__main__":
    build()
