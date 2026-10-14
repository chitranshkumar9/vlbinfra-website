"""Builds the VLB website pages from the content below.

Run from the repository root:  python3 tools/build.py
Edit the CONTENT section, re-run, and commit the generated .html files.
"""
import hashlib
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ============================ CONTENT ============================

PHONE_DISPLAY = "+91 80776 76214"
PHONE_TEL = "+918077676214"
WHATSAPP = "918077676214"
EMAIL = "info@vlbinfra.com"
ADDRESS = "3/2561, Dehradun Road, Janak Nagar, Saharanpur, Uttar Pradesh 247001"
MAPS = "https://www.google.com/maps/search/?api=1&query=3%2F2561+Dehradun+Road+Janak+Nagar+Saharanpur+247001"

REGISTRATION = "A+ / Class 1"          # e.g. "Class A — UP PWD"
YEARS = "30+"

# Departments VLB has worked for. Leave empty to show the general line only.
DEPARTMENTS = []                    # e.g. ["UP PWD", "Irrigation Department", ...]

SERVICES = [
    {
        "id": "roads", "icon": "road", "name": "Roads, Highways & Bypasses",
        "short": "New roads, highways, bypasses, widening and strengthening works.",
        "scope": ["Highways", "Bypasses", "New road construction", "Widening & strengthening",
                  "CC & bituminous roads", "Resurfacing & maintenance"],
    },
    {
        "id": "bridges", "icon": "bridge", "name": "Bridges",
        "short": "Bridges and cross-structures for road and irrigation projects.",
        "scope": ["Major & minor bridges", "Girder bridges", "Culverts", "Cross-structures",
                  "Approach roads", "Protection works"],
    },
    {
        "id": "irrigation", "icon": "canal", "name": "Irrigation Works",
        "short": "Canal and irrigation works for state irrigation departments.",
        "scope": ["Canal construction", "Canal lining", "Head regulators & falls",
                  "Cross-drainage works", "Embankments", "Repair & strengthening"],
    },
    {
        "id": "education", "icon": "school", "name": "Schools & Colleges",
        "short": "School, college and campus buildings for education departments.",
        "scope": ["School buildings", "College buildings", "Classroom blocks",
                  "Hostels", "Boundary walls & gates", "Finishing & services"],
    },
    {
        "id": "buildings", "icon": "building", "name": "Government Buildings",
        "short": "Offices and institutional buildings for government departments.",
        "scope": ["Administrative offices", "Institutional buildings", "Staff quarters",
                  "RCC framed structures", "Boundary walls & gates", "Finishing & services"],
    },
    {
        "id": "drainage", "icon": "drain", "name": "Drainage Works",
        "short": "Covered and open drains, nalas, storm-water and sewer line works.",
        "scope": ["Covered & open drains", "Nala construction", "Storm-water drainage",
                  "Sewer lines", "Desilting & repair", "Urban drainage"],
    },
]

# Machinery & resources (types only, no counts)
MACHINERY = [
    ("Earthwork & road machinery", "road",
     ["JCB / backhoe loaders", "Excavators", "Motor graders", "Vibratory & tandem road rollers",
      "Hot mix plant", "Paver finishers", "Water tankers"]),
    ("Concrete & building", "tower",
     ["Concrete mixers", "Transit mixers", "Batching plant", "Needle & plate vibrators",
      "Steel shuttering & scaffolding"]),
    ("Transport & lifting", "truck",
     ["Tipper & dumper trucks", "Tractor-trolleys", "Hydra cranes"]),
    ("Survey & testing", "survey",
     ["Total stations", "Auto levels", "Site laboratory: cube, slump and sieve tests"]),
]

# Careers: roles VLB hires for. Set "open": True for a role with a current vacancy.
CAREER_ROLES = [
    {"title": "Site Engineer (Civil)", "type": "Full time", "location": "Delhi NCR sites",
     "summary": "Runs day-to-day execution on site: layout, RCC and road works, quality checks, measurements and daily reporting.",
     "needs": "B.Tech / Diploma in Civil Engineering", "open": False},
    {"title": "Site Supervisor", "type": "Full time", "location": "Delhi NCR sites",
     "summary": "Manages labour, materials and daily progress on site, working with the site engineer.",
     "needs": "Experience on civil construction sites", "open": False},
    {"title": "Billing & Quantity Engineer", "type": "Full time", "location": "Office + sites",
     "summary": "Prepares measurements, running bills and BOQ quantities for government works.",
     "needs": "Civil Engineering background; knowledge of government billing", "open": False},
    {"title": "Surveyor", "type": "Full time", "location": "Delhi NCR sites",
     "summary": "Levels, alignments and setting-out for roads, bridges, canals and buildings.",
     "needs": "Experience with auto level / total station", "open": False},
]

# Projects. Add one entry per project; photos go in images/projects/.
# status: "done" or "ongoing".  category: one of the SERVICES names.
PROJECTS = [
    {
        "name": "Bridge construction",
        "category": "Bridges & Culverts",
        "photos": ["images/projects/bridge-girders.jpg", "images/projects/bridge-girders-2.jpg"],
        "featured": True,
    },
    {
        "name": "Institutional building",
        "category": "Government Buildings",
        "photos": ["images/projects/institutional-building.jpg"],
        "featured": True,
    },
    {
        "name": "Road resurfacing",
        "category": "Roads & Highways",
        "photos": ["images/projects/road-resurfacing-night.jpg"],
        "featured": True,
    },
    # Template:
    # {
    #     "name": "Construction of CC road, Ward 12",
    #     "category": "CC Roads & Paving",
    #     "place": "Saharanpur",
    #     "department": "Nagar Nigam Saharanpur",
    #     "year": "2024",
    #     "value": "",              # e.g. "₹2.4 Cr" or leave empty
    #     "status": "done",
    #     "photo": "images/projects/cc-road-ward-12.jpg",
    #     "featured": True,
    # },
]

# ============================ TEMPLATES ============================

ICONS = {
    "road": '<path d="M14 4L6 36M26 4l8 32M20 6v5M20 17v6M20 29v5"/>',
    "building": '<path d="M4 34h32M6 34V14l14-8 14 8v20M12 34V20M20 34V20M28 34V20M6 14h28"/>',
    "bridge": '<path d="M2 16h36M4 16v14M36 16v14M8 30c0-8 5-12 12-12s12 4 12 12M2 30h36"/>',
    "canal": '<path d="M2 12h8l6 16h8l6-16h8M10 12l6 16M30 12l-6 16M4 34h32M12 22h16"/>',
    "school": '<path d="M4 34h32M7 34V18h26v16M4 18l16-10 16 10M17 34v-8h6v8M11 22h3M26 22h3M20 13v.5"/>',
    "drain": '<path d="M6 8v16a14 14 0 0 0 28 0V8M6 8h6M28 8h6M12 8v16a8 8 0 0 0 16 0V8M14 30c2 1 4 1.5 6 1.5"/>',
    "paving": '<path d="M4 6h32v28H4zM4 15h32M4 25h32M15 6v9M25 15v10M15 25v9"/>',
    "truck": '<path d="M2 26V12h20v14M22 16h8l6 6v4H22M2 26h34M9 30a3 3 0 1 0 0 .1M29 30a3 3 0 1 0 0 .1"/>',
    "survey": '<path d="M20 6v8M14 14h12l-2 6h-8zM20 20v14M12 34l8-14 8 14"/>',
    "tower": '<path d="M8 36V12l8-4v28M16 36V4h10v32M26 36V14h8v22M4 36h32M19 10h4M19 16h4M19 22h4M19 28h4"/>',
}
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M4 12.5l5 5L20 6.5"/></svg>'
PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
WA_SVG = '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2s.2-1.1.2-1.2-.2-.2-.5-.3z"/></svg>'
SKYLINE = '''<svg class="skyline" viewBox="0 0 600 420" fill="none" stroke="#c49a3e" stroke-width="3" aria-hidden="true">
      <path d="M40 420V250h90v170M130 420V150l70-40v310M200 420V60h80v360M280 420V180h70v240M350 420V120l90 40v260M440 420V230h110v190"/>
      <path d="M220 100h40M220 150h40M220 200h40M220 250h40M220 300h40M370 170h50M370 220h50M370 270h50M370 320h50M150 190h30M150 240h30M150 290h30"/>
    </svg>'''

NAV = [("index.html", "Home"), ("about.html", "About"), ("services.html", "Services")]
SHOW_PROJECTS = False   # set True to bring back the Projects page and the home "Recent works" section
if SHOW_PROJECTS:
    NAV.append(("projects.html", "Projects"))
NAV.append(("machinery.html", "Machinery"))
NAV.append(("careers.html", "Careers"))

e = html.escape


def asset_version(rel):
    """Short content hash so browsers fetch a fresh copy whenever the file changes."""
    return hashlib.sha1((ROOT / rel).read_bytes()).hexdigest()[:8]


def icon(name, size=40):
    return f'<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">{ICONS[name]}</svg>'


def page(filename, title, description, body):
    links = "\n".join(
        f'      <a href="{href}"{" aria-current=\"page\"" if href == filename else ""}>{label}</a>'
        for href, label in NAV)
    cta_current = ' aria-current="page"' if filename == "contact.html" else ""
    tab_title = "VLB" if filename == "index.html" else f"{title} | VLB"
    full_title = "Vaibhav Laxmi Builders (VLB) — Government Civil Contractor, Delhi NCR" if filename == "index.html" else f"{title} | Vaibhav Laxmi Builders (VLB)"
    svc_links = "\n".join(f'          <li><a href="services.html#{s["id"]}">{e(s["name"])}</a></li>' for s in SERVICES)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<script>try{{var t=localStorage.getItem("vlb-theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<meta name="theme-color" content="#14233f">
<title>{e(tab_title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.vlbinfra.com/{'' if filename == 'index.html' else filename}">
<meta property="og:image" content="https://www.vlbinfra.com/assets/logo.png">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/style.css?v={asset_version('assets/style.css')}">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Vaibhav Laxmi Builders home">
      <span class="mark"><img src="assets/logo.svg" alt="VLB logo"></span>
      <span><b>Vaibhav Laxmi Builders</b><small>Govt. Civil Contractor · Delhi NCR</small></span>
    </a>
    <button class="theme-btn" type="button" aria-label="Switch to dark mode" title="Dark / light mode">
      <svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
      <svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 1.5v2.5M12 20v2.5M4.6 4.6l1.8 1.8M17.6 17.6l1.8 1.8M1.5 12H4M20 12h2.5M4.6 19.4l1.8-1.8M17.6 6.4l1.8-1.8"/></svg>
    </button>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav" id="site-nav" aria-label="Main">
{links}
      <a class="cta" href="contact.html"{cta_current}>Contact</a>
    </nav>
  </div>
</header>

<main>
{body}
</main>

<footer class="foot">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="index.html">
          <span class="mark"><img src="assets/logo.svg" alt=""></span>
          <span><b>Vaibhav Laxmi Builders</b><small>VLB · Delhi NCR</small></span>
        </a>
        <p>Government civil contractor executing roads, highways, bridges, irrigation works and government buildings across Delhi NCR.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
{svc_links}
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li>{e(ADDRESS)}</li>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="base">
      <span>© 2026 Vaibhav Laxmi Builders (VLB). All rights reserved.</span>
      <span>vlbinfra.com</span>
    </div>
  </div>
</footer>

<a class="wa" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WA_SVG}</a>
<script src="assets/site.js?v={asset_version('assets/site.js')}"></script>
</body>
</html>
'''


def page_hero(crumb, title, lede):
    return f'''  <section class="page-hero">
    {SKYLINE}
    <div class="wrap">
      <span class="crumbs"><a href="index.html">Home</a> / {e(crumb)}</span>
      <h1>{title}</h1>
      <p>{lede}</p>
    </div>
  </section>'''


def particulars():
    return f'''      <aside class="sheet" aria-label="Contractor particulars">
        <h2>Contractor particulars</h2>
        <dl>
          <dt>Firm</dt><dd>Vaibhav Laxmi Builders</dd>
          <dt>Category</dt><dd>Government civil contractor</dd>
          <dt>Registration</dt><dd>{e(REGISTRATION)}</dd>
          <dt>Works for</dt><dd>Delhi NCR Govt. departments</dd>
        </dl>
      </aside>'''


def dept_band():
    tags = DEPARTMENTS or ["State Government", "Central Government"]
    tag_html = "".join(f"<span>{e(t)}</span>" for t in tags)
    return f'''  <section class="dept">
    <div class="wrap">
      <div><span class="eyebrow">Who we build for</span><h2>Trusted by government departments</h2></div>
      <div>
        <p style="margin-bottom:22px">VLB has executed works for State and Central Government departments across Delhi NCR.</p>
        <div class="tags">{tag_html}</div>
      </div>
    </div>
  </section>'''


def cta_band():
    return f'''  <section class="cta-band">
    <div class="wrap">
      <div><h2>Discuss a work with us</h2><p>Tenders, enquiries, vendor and subcontracting partnerships.</p></div>
      <div class="actions">
        <a class="btn btn-gold" href="tel:{PHONE_TEL}">{PHONE_SVG}{PHONE_DISPLAY}</a>
        <a class="btn btn-ghost" href="contact.html">All contact details</a>
      </div>
    </div>
  </section>'''


def project_card(p):
    status = {"done": '<span class="status done">Completed</span>',
              "ongoing": '<span class="status ongoing">Ongoing</span>'}.get(p.get("status"), "")
    rows = [("Location", p.get("place")), ("Department", p.get("department")),
            ("Year", p.get("year")), ("Value", p.get("value"))]
    dl = "".join(f"<dt>{k}</dt><dd>{e(v)}</dd>" for k, v in rows if v)
    dl = f"<dl>{dl}</dl>" if dl else ""
    photos = p.get("photos") or ([p["photo"]] if p.get("photo") else [])
    photo = ""
    if photos:
        photo = f'<img src="{e(photos[0])}" alt="{e(p["name"])}" loading="lazy">'
        if len(photos) > 1:
            photo = (f'<button type="button" class="ph-next" data-photos="{e("|".join(photos))}" '
                     f'aria-label="Next photo of {e(p["name"])}">{photo}<span>1 / {len(photos)}</span></button>')
    return f'''        <article class="proj" data-cat="{e(p.get("category", ""))}">
          <div class="ph">{photo}</div>
          <div class="body">
            <span class="cat">{e(p.get("category", ""))}</span>
            <h3>{e(p["name"])}</h3>
            {status}
            {dl}
          </div>
        </article>'''


def empty_projects():
    return f'''      <div class="empty">
        <h3>Project portfolio being updated</h3>
        <p>Photographs and details of our completed government works are being added. For our full list of completed and ongoing works, <a href="contact.html">contact our office</a>.</p>
      </div>'''


# ============================ PAGES ============================

def home():
    featured = [p for p in PROJECTS if p.get("featured")][:3] or PROJECTS[:3]
    proj = (f'<div class="proj-grid">\n' + "\n".join(project_card(p) for p in featured) + "\n      </div>") if featured else empty_projects()
    proj_section = (f'''  <section class="block">
    <div class="wrap">
      <div class="head">
        <div><span class="eyebrow">Projects</span><h2>Recent works</h2></div>
        <p>A selection of government works executed by VLB.</p>
      </div>
      {proj}
      <a class="more" href="projects.html">All projects →</a>
    </div>
  </section>

''') if SHOW_PROJECTS else ""
    svc = "\n".join(f'        <a href="services.html#{s["id"]}">{icon(s["icon"])}{e(s["name"])}</a>' for s in SERVICES)
    body = f'''  <section class="hero hero-logo">
    {SKYLINE}
    <div class="wrap">
      <div>
        <img class="hero-logo-img" src="assets/logo-light.svg" alt="VLB – Vaibhav Laxmi Builders">
        <h1 class="sr-only">VLB – Vaibhav Laxmi Builders</h1>
        <p class="hero-tag">Government civil contractor · <em>Roads · Bridges · Irrigation · Buildings</em></p>
        <p class="lede">Vaibhav Laxmi Builders executes roads, highways, bridges, irrigation works, schools, colleges and government buildings for State and Central Government departments across Delhi NCR.</p>
        <div class="actions">
          <a class="btn btn-gold" href="about.html">About VLB</a>
          <a class="btn btn-ghost" href="contact.html#enquiry">Send an enquiry</a>
        </div>
      </div>
{particulars()}
    </div>
  </section>

  <div class="strip">
    <div class="wrap">
      <div class="stat"><b>100%</b><span>On-time delivery</span></div>
      <div class="stat"><b>{e(REGISTRATION)}</b><span>Government contractor registration</span></div>
      <div class="stat"><b>State &amp; Central</b><span>Departments served across Delhi NCR</span></div>
    </div>
  </div>

  <section class="block">
    <div class="wrap">
      <div class="about-grid">
        <div>
          <span class="eyebrow">About VLB</span>
          <p class="big" style="margin-top:16px">We build the roads and bridges people travel on, the canals that water the fields, and the schools and offices where government serves the public.</p>
        </div>
        <div>
          <p>VLB is an A+ / Class 1 registered government contractor, trusted by State and Central Government departments across Delhi NCR with roads, bridges, irrigation works and public buildings.</p>
          <p>Every project is run to the department's drawings, specifications and timelines, with our own site teams, supervisors and machinery.</p>
          <a class="more" href="about.html">More about VLB →</a>
        </div>
      </div>
    </div>
  </section>

  <section class="block" style="padding-top:0">
    <div class="wrap">
      <div class="head">
        <div><span class="eyebrow">Services</span><h2>What we build</h2></div>
        <p>Civil works for government departments, from highways and bridges to irrigation works and public buildings.</p>
      </div>
      <div class="svc-mini">
{svc}
      </div>
      <a class="more" href="services.html">All services →</a>
    </div>
  </section>

{dept_band()}

{proj_section}{cta_band()}'''
    return page("index.html", "Home",
                "Vaibhav Laxmi Builders (VLB): A+ / Class 1 government civil contractor for roads, highways, bridges, irrigation works, schools, colleges and government buildings across Delhi NCR.",
                body)


def about():
    body = f'''{page_hero("About", "About VLB", "A+ / Class 1 government civil contractor executing public works for State and Central Government departments across Delhi NCR.")}

  <section class="block">
    <div class="wrap">
      <div class="about-grid">
        <div>
          <span class="eyebrow">Our story</span>
          <p class="big" style="margin-top:16px">Building the public infrastructure of Delhi NCR.</p>
        </div>
        <div>
          <p>Vaibhav Laxmi Builders is an A+ / Class 1 registered government contractor, trusted by State and Central Government departments across Delhi NCR with roads, highways, bypasses, bridges, irrigation works, schools, colleges and government buildings.</p>
          <p>We work to the department's drawings, specifications and timelines, with our own engineers, supervisors, labour and machinery on every site.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="block" style="padding-top:0">
    <div class="wrap">
      <div class="head">
        <div><span class="eyebrow">How we work</span><h2>What sets VLB apart</h2></div>
        <p>The standards we hold on every government work we take up.</p>
      </div>
      <ul class="checks" style="max-width:820px">
        <li>{CHECK}<span><b>Specification-first execution.</b> Work done to department drawings, schedules and quality norms.</span></li>
        <li>{CHECK}<span><b>100% on-time delivery.</b> Every work handed over to the department on schedule.</span></li>
        <li>{CHECK}<span><b>Own teams on site.</b> Experienced engineers, supervisors and labour managed directly by VLB.</span></li>
        <li>{CHECK}<span><b>Timely handover.</b> Planned mobilisation and daily progress tracking until completion.</span></li>
      </ul>
    </div>
  </section>

  <section class="block" style="padding-top:0">
    <div class="wrap">
      <div class="head">
        <div><span class="eyebrow">Process</span><h2>From tender to handover</h2></div>
        <p>The same disciplined sequence on every work.</p>
      </div>
      <ol class="steps">
        <li><h3>Tender &amp; award</h3><p>Careful study of the scope, drawings and BOQ before every bid.</p></li>
        <li><h3>Mobilisation</h3><p>Site setup, material sourcing, machinery and teams deployed quickly after award.</p></li>
        <li><h3>Execution &amp; QC</h3><p>Work to specification, with regular quality checks and progress reporting.</p></li>
        <li><h3>Measurement &amp; handover</h3><p>Joint measurements, documentation and handover to the department.</p></li>
      </ol>
    </div>
  </section>

{dept_band()}

{cta_band()}'''
    return page("about.html", "About", "About Vaibhav Laxmi Builders (VLB): A+ / Class 1 government civil contractor executing public works across Delhi NCR.", body)


def services():
    rows = "\n".join(f'''        <article class="svc-row" id="{s["id"]}">
          {icon(s["icon"])}
          <div><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></div>
          <ul class="scope">{"".join(f"<li>{e(x)}</li>" for x in s["scope"])}</ul>
        </article>''' for s in SERVICES)
    body = f'''{page_hero("Services", "Services", "Civil works for government departments, from highways and bridges to irrigation works and public buildings.")}

  <section class="block">
    <div class="wrap">
      <div class="svc-list">
{rows}
      </div>
    </div>
  </section>

{cta_band()}'''
    return page("services.html", "Services", "Services of Vaibhav Laxmi Builders: roads, highways and bypasses, bridges, irrigation works, schools and colleges, and government buildings.", body)


def projects():
    if PROJECTS:
        cats = sorted({p["category"] for p in PROJECTS if p.get("category")})
        filt = ('<div class="filters" role="group" aria-label="Filter projects"><button type="button" aria-pressed="true" data-filter="all">All</button>'
                + "".join(f'<button type="button" aria-pressed="false" data-filter="{e(c)}">{e(c)}</button>' for c in cats) + "</div>") if len(cats) > 1 else ""
        content = f'''{filt}
      <div class="proj-grid">
{chr(10).join(project_card(p) for p in PROJECTS)}
      </div>'''
    else:
        content = empty_projects()
    body = f'''{page_hero("Projects", "Projects", "Government works executed by Vaibhav Laxmi Builders across Delhi NCR.")}

  <section class="block">
    <div class="wrap">
      {content}
    </div>
  </section>

{cta_band()}'''
    return page("projects.html", "Projects", "Completed and ongoing government projects by Vaibhav Laxmi Builders (VLB) across Delhi NCR.", body)


def machinery():
    blocks = "\n".join(f"""        <article class="mach">
          <div class="mach-head">{icon(ic)}<h2>{e(title)}</h2></div>
          <ul class="scope">{"".join(f"<li>{e(x)}</li>" for x in items)}</ul>
        </article>""" for title, ic, items in MACHINERY)
    body = f"""{page_hero("Machinery", "Machinery &amp; resources", "Our own fleet, site teams and testing set-up, so works move on schedule without depending on hired equipment.")}

  <section class="block">
    <div class="wrap">
      <div class="head">
        <div><span class="eyebrow">Our fleet</span><h2>Owned and run by VLB</h2></div>
        <p>VLB executes works with its own machinery and operators, from earthwork and road laying to concrete, lifting and survey.</p>
      </div>
      <div class="mach-grid">
{blocks}
      </div>
    </div>
  </section>

  <section class="block" style="padding-top:0">
    <div class="wrap">
      <div class="head">
        <div><span class="eyebrow">People</span><h2>Teams on every site</h2></div>
        <p>Machinery is only as good as the people running it.</p>
      </div>
      <ul class="checks" style="max-width:820px">
        <li>{CHECK}<span><b>Site engineers.</b> Responsible for execution, quality checks and measurements on each work.</span></li>
        <li>{CHECK}<span><b>Supervisors.</b> Manage labour, materials and daily progress on site.</span></li>
        <li>{CHECK}<span><b>Trained operators.</b> Our own operators for rollers, pavers, excavators and plants.</span></li>
        <li>{CHECK}<span><b>Skilled workforce.</b> Masons, steel fixers, carpenters and helpers deployed as each work needs.</span></li>
      </ul>
    </div>
  </section>

{cta_band()}"""
    return page("machinery.html", "Machinery", "Machinery and resources of Vaibhav Laxmi Builders (VLB): own fleet of road, earthwork, concrete, transport and survey equipment.", body)


def careers():
    import urllib.parse as up
    def mail(subject, body):
        return "mailto:" + EMAIL + "?subject=" + up.quote(subject) + "&body=" + up.quote(body)
    cards = [
        ("Real government works", "Work on roads, bridges, irrigation works and public buildings for State and Central Government departments."),
        ("Learn on site", "Hands-on experience from setting-out to final measurement, alongside experienced engineers and supervisors."),
        ("Safety first", "Safety equipment and clear site practices on every work we execute."),
        ("Grow with us", "Responsibility grows with performance. Good engineers move up to run their own sites."),
    ]
    why = "\n".join(f"""        <div class="why"><h3>{e(t)}</h3><p>{e(d)}</p></div>""" for t, d in cards)
    roles = []
    for r in CAREER_ROLES:
        badge = '<span class="status ongoing">Hiring now</span>' if r.get("open") else ""
        href = mail(f"Application: {r['title']}", f"Hello VLB team,\n\nI would like to apply for the {r['title']} role.\n\nName:\nPhone:\nExperience:\n\n(Please attach your resume.)")
        roles.append(f"""        <article class="role">
          <div class="role-main">
            <h3>{e(r['title'])}</h3>
            <p>{e(r['summary'])}</p>
            <ul class="role-meta"><li>{e(r['type'])}</li><li>{e(r['location'])}</li><li>{e(r['needs'])}</li></ul>
          </div>
          <div class="role-act">{badge}<a class="btn btn-navy" href="{e(href)}">Apply →</a></div>
        </article>""")
    general = mail("Resume for VLB", "Hello VLB team,\n\nI would like to work with Vaibhav Laxmi Builders.\n\nName:\nPhone:\nRole I am interested in:\nExperience:\n\n(Please attach your resume.)")
    body = f"""{page_hero("Careers", "Build your career with VLB", "We hire engineers, supervisors and site teams for government works across Delhi NCR.")}

  <section class="block">
    <div class="wrap">
      <div class="head">
        <div><span class="eyebrow">Why VLB</span><h2>Work that gets built</h2></div>
        <p>What you can expect when you join our team.</p>
      </div>
      <div class="why-grid">
{why}
      </div>
    </div>
  </section>

  <section class="block" id="roles" style="padding-top:0">
    <div class="wrap">
      <div class="head">
        <div><span class="eyebrow">Roles</span><h2>Who we hire</h2></div>
        <p>The roles we regularly hire for. Send your resume for any of them and we will contact you when there is a vacancy.</p>
      </div>
      <div class="roles">
{chr(10).join(roles)}
      </div>
    </div>
  </section>

  <section class="block" style="padding-top:0">
    <div class="wrap">
      <div class="enquiry">
        <div>
          <span class="eyebrow">Apply</span>
          <h2>Don't see your role?</h2>
          <p>Send us your resume anyway. Email it to <b>{EMAIL}</b> or share it on WhatsApp at <b>{PHONE_DISPLAY}</b>.</p>
        </div>
        <div class="apply-actions">
          <a class="btn btn-gold" href="{e(general)}">Email your resume</a>
          <a class="btn btn-navy" href="https://wa.me/{WHATSAPP}?text={up.quote('Hello VLB team, I would like to share my resume for a job at Vaibhav Laxmi Builders.')}" target="_blank" rel="noopener">Send on WhatsApp</a>
        </div>
      </div>
    </div>
  </section>"""
    return page("careers.html", "Careers", "Careers at Vaibhav Laxmi Builders (VLB): site engineer, supervisor, billing and survey roles on government works across Delhi NCR.", body)


def contact():
    body = f'''{page_hero("Contact", "Contact us", "For tenders, enquiries, vendor and subcontracting partnerships, call or write to us.")}

  <section class="block">
    <div class="wrap">
      <div class="contact">
        <div class="card">
          <span class="k">Address</span>
          <span class="v">{e(ADDRESS)}</span>
          <a class="go" href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps →</a>
        </div>
        <div class="card">
          <span class="k">Phone &amp; WhatsApp</span>
          <span class="v">{PHONE_DISPLAY}</span>
          <a class="go" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">Message on WhatsApp →</a>
        </div>
        <div class="card">
          <span class="k">Email</span>
          <span class="v">{EMAIL}</span>
          <a class="go" href="mailto:{EMAIL}">Write to us →</a>
        </div>
      </div>
    </div>
  </section>

  <section class="block" id="enquiry" style="padding-top:0">
    <div class="wrap">
      <div class="enquiry">
        <div>
          <span class="eyebrow">Enquiry</span>
          <h2>Send an enquiry</h2>
          <p>Fill in your details and send them to us on WhatsApp or by email. We usually reply within one working day.</p>
        </div>
        <form id="enquiry-form" novalidate>
          <div class="field"><label for="enq-name">Your name</label><input id="enq-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="enq-org">Organisation / department <small>(optional)</small></label><input id="enq-org" name="org" autocomplete="organization"></div>
          <div class="field"><label for="enq-phone">Phone</label><input id="enq-phone" name="phone" type="tel" autocomplete="tel" required></div>
          <div class="field"><label for="enq-email">Email <small>(optional)</small></label><input id="enq-email" name="email" type="email" autocomplete="email"></div>
          <div class="field full"><label for="enq-msg">Your enquiry</label><textarea id="enq-msg" name="message" rows="5" required></textarea></div>
          <p class="form-error full" id="enq-error" role="alert" hidden>Please fill in your name, phone and enquiry.</p>
          <div class="actions full">
            <button class="btn btn-gold" type="submit" data-via="whatsapp">Send on WhatsApp</button>
            <button class="btn btn-navy" type="submit" data-via="email">Send by email</button>
          </div>
        </form>
      </div>
    </div>
  </section>'''
    return page("contact.html", "Contact", "Contact Vaibhav Laxmi Builders (VLB). Phone +91 80776 76214, email info@vlbinfra.com.", body)


if __name__ == "__main__":
    pages = [("index.html", home), ("about.html", about), ("services.html", services), ("machinery.html", machinery), ("careers.html", careers), ("contact.html", contact)]
    if SHOW_PROJECTS:
        pages.append(("projects.html", projects))
    else:
        (ROOT / "projects.html").write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=index.html">'
            '<link rel="canonical" href="https://www.vlbinfra.com/"><title>VLB</title></head>'
            '<body><p><a href="index.html">Go to the Vaibhav Laxmi Builders home page</a></p></body></html>\n',
            encoding="utf-8")
    for name, fn in pages:
        (ROOT / name).write_text(fn(), encoding="utf-8")
        print("built", name)
