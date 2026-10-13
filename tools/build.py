"""Builds the VLB website pages from the content below.

Run from the repository root:  python3 tools/build.py
Edit the CONTENT section, re-run, and commit the generated .html files.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ============================ CONTENT ============================

PHONE_DISPLAY = "+91 98370 16102"
PHONE_TEL = "+919837016102"
WHATSAPP = "919837016102"
EMAIL = "info@vlbinfra.com"
ADDRESS = "3/2561, Dehradun Road, Janak Nagar, Saharanpur, Uttar Pradesh 247001"
MAPS = "https://www.google.com/maps/search/?api=1&query=3%2F2561+Dehradun+Road+Janak+Nagar+Saharanpur+247001"

REGISTRATION = "Top class"          # e.g. "Class A — UP PWD"
YEARS = "30+"

# Departments VLB has worked for. Leave empty to show the general line only.
DEPARTMENTS = []                    # e.g. ["UP PWD", "Irrigation Department", ...]

SERVICES = [
    {
        "id": "roads", "icon": "road", "name": "Roads & Highways",
        "short": "Bituminous roads, widening and strengthening, link roads and highway works.",
        "scope": ["New bituminous roads", "Widening & strengthening", "Rural & link roads",
                  "Highway works", "Resurfacing & maintenance", "Road furniture & markings"],
    },
    {
        "id": "buildings", "icon": "building", "name": "Government Buildings",
        "short": "Offices, schools, hospitals, residential quarters and institutional buildings.",
        "scope": ["Administrative offices", "Schools & colleges", "Hospitals & health centres",
                  "Staff quarters", "Boundary walls & gates", "Finishing & services"],
    },
    {
        "id": "bridges", "icon": "bridge", "name": "Bridges & Culverts",
        "short": "Minor bridges, box and pipe culverts, causeways and cross-drainage structures.",
        "scope": ["Minor bridges", "Box culverts", "Pipe culverts", "Causeways",
                  "Cross-drainage works", "Protection works"],
    },
    {
        "id": "drainage", "icon": "drain", "name": "Drainage Works",
        "short": "Covered and open drains, nalas, storm-water and sewer line works.",
        "scope": ["Covered & open drains", "Nala construction", "Storm-water drainage",
                  "Sewer lines", "Desilting & repair", "Urban drainage"],
    },
    {
        "id": "cc-roads", "icon": "paving", "name": "CC Roads & Paving",
        "short": "Cement concrete roads, interlocking tile paving and internal streets.",
        "scope": ["Cement concrete roads", "Interlocking paver blocks", "Internal streets",
                  "Kerbs & footpaths", "Parking areas", "Colony development"],
    },
    {
        "id": "high-rise", "icon": "tower", "name": "Commercial & High-Rise",
        "short": "Multi-storey commercial and public buildings, from foundation to finishing.",
        "scope": ["RCC framed structures", "Foundations", "Multi-storey buildings",
                  "Commercial complexes", "Structural works", "Finishing works"],
    },
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
    "drain": '<path d="M6 8v16a14 14 0 0 0 28 0V8M6 8h6M28 8h6M12 8v16a8 8 0 0 0 16 0V8M14 30c2 1 4 1.5 6 1.5"/>',
    "paving": '<path d="M4 6h32v28H4zM4 15h32M4 25h32M15 6v9M25 15v10M15 25v9"/>',
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

e = html.escape


def icon(name, size=40):
    return f'<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">{ICONS[name]}</svg>'


def page(filename, title, description, body):
    links = "\n".join(
        f'      <a href="{href}"{" aria-current=\"page\"" if href == filename else ""}>{label}</a>'
        for href, label in NAV)
    cta_current = ' aria-current="page"' if filename == "contact.html" else ""
    full_title = "Vaibhav Laxmi Builders (VLB) — Government Civil Contractor, Saharanpur" if filename == "index.html" else f"{title} | Vaibhav Laxmi Builders (VLB)"
    svc_links = "\n".join(f'          <li><a href="services.html#{s["id"]}">{e(s["name"])}</a></li>' for s in SERVICES)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://www.vlbinfra.com/{'' if filename == 'index.html' else filename}">
<meta property="og:image" content="https://www.vlbinfra.com/assets/logo.png">
<link rel="icon" href="assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Vaibhav Laxmi Builders home">
      <span class="mark"><img src="assets/logo.png" alt="VLB logo"></span>
      <span><b>Vaibhav Laxmi Builders</b><small>Govt. Civil Contractor · Saharanpur</small></span>
    </a>
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
          <span class="mark"><img src="assets/logo.png" alt=""></span>
          <span><b>Vaibhav Laxmi Builders</b><small>VLB · Saharanpur, U.P.</small></span>
        </a>
        <p>Government civil contractor executing roads, bridges, drainage and government buildings across Uttar Pradesh.</p>
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
<script src="assets/site.js"></script>
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
          <dt>Experience</dt><dd>{YEARS} years</dd>
          <dt>Works for</dt><dd>UP State &amp; Central Govt.</dd>
          <dt>Head office</dt><dd>Saharanpur, U.P.</dd>
        </dl>
      </aside>'''


def dept_band():
    tags = DEPARTMENTS or ["Uttar Pradesh Government", "Central Government"]
    tag_html = "".join(f"<span>{e(t)}</span>" for t in tags)
    return f'''  <section class="dept">
    <div class="wrap">
      <div><span class="eyebrow">Who we build for</span><h2>Trusted by government departments</h2></div>
      <div>
        <p style="margin-bottom:22px">VLB has executed works for leading departments of the Government of Uttar Pradesh and the Central Government.</p>
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
    body = f'''  <section class="hero">
    {SKYLINE}
    <div class="wrap">
      <div>
        <span class="eyebrow">Government Civil Contractor · Uttar Pradesh</span>
        <h1>Building public works <em>for over 30 years</em></h1>
        <p class="lede">Vaibhav Laxmi Builders executes roads, bridges, drainage and government buildings for departments of the Uttar Pradesh and Central Government, from our head office in Saharanpur.</p>
        <div class="actions">
          <a class="btn btn-gold" href="tel:{PHONE_TEL}">{PHONE_SVG}{PHONE_DISPLAY}</a>
          <a class="btn btn-ghost" href="about.html">About VLB</a>
        </div>
      </div>
{particulars()}
    </div>
  </section>

  <div class="strip">
    <div class="wrap">
      <div class="stat"><b>{YEARS}</b><span>Years of executing government works</span></div>
      <div class="stat"><b>{e(REGISTRATION)}</b><span>Government contractor registration</span></div>
      <div class="stat"><b>State &amp; Central</b><span>Departments served across Uttar Pradesh</span></div>
    </div>
  </div>

  <section class="block">
    <div class="wrap">
      <div class="about-grid">
        <div>
          <span class="eyebrow">About VLB</span>
          <p class="big" style="margin-top:16px">We build the roads people drive on, the drains that keep towns dry, and the buildings where government serves the public.</p>
        </div>
        <div>
          <p>Founded and led by the same family for over thirty years, VLB has grown from a Saharanpur contracting firm into a top-class registered government contractor trusted with large public works.</p>
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
        <p>Civil works for government departments, from rural link roads to multi-storey public buildings.</p>
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
                "Vaibhav Laxmi Builders (VLB), Saharanpur: government civil contractor with 30+ years of experience in roads, bridges, drainage and government buildings across Uttar Pradesh.",
                body)


def about():
    body = f'''{page_hero("About", "About VLB", "A family-run government civil contractor from Saharanpur, executing public works across Uttar Pradesh for over 30 years.")}

  <section class="block">
    <div class="wrap">
      <div class="about-grid">
        <div>
          <span class="eyebrow">Our story</span>
          <p class="big" style="margin-top:16px">Three decades of building the public infrastructure of Western Uttar Pradesh.</p>
        </div>
        <div>
          <p>Vaibhav Laxmi Builders was founded in Saharanpur and has been led by the same family for over thirty years. What began as a local contracting firm is today a top-class registered government contractor, trusted by departments of the Uttar Pradesh and Central Government with roads, bridges, drainage and public buildings.</p>
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
        <li>{CHECK}<span><b>Local roots.</b> Based in Saharanpur, with deep knowledge of working conditions across Western Uttar Pradesh.</span></li>
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
    return page("about.html", "About", "About Vaibhav Laxmi Builders (VLB): a family-run government civil contractor in Saharanpur with over 30 years of public works experience.", body)


def services():
    rows = "\n".join(f'''        <article class="svc-row" id="{s["id"]}">
          {icon(s["icon"])}
          <div><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></div>
          <ul class="scope">{"".join(f"<li>{e(x)}</li>" for x in s["scope"])}</ul>
        </article>''' for s in SERVICES)
    body = f'''{page_hero("Services", "Services", "Civil works for government departments, from rural link roads to multi-storey public buildings.")}

  <section class="block">
    <div class="wrap">
      <div class="svc-list">
{rows}
      </div>
    </div>
  </section>

{cta_band()}'''
    return page("services.html", "Services", "Services of Vaibhav Laxmi Builders: roads and highways, government buildings, bridges and culverts, drainage, CC roads and high-rise construction.", body)


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
    body = f'''{page_hero("Projects", "Projects", "Government works executed by Vaibhav Laxmi Builders across Uttar Pradesh.")}

  <section class="block">
    <div class="wrap">
      {content}
    </div>
  </section>

{cta_band()}'''
    return page("projects.html", "Projects", "Completed and ongoing government projects by Vaibhav Laxmi Builders (VLB) across Uttar Pradesh.", body)


def contact():
    body = f'''{page_hero("Contact", "Contact us", "For tenders, enquiries, vendor and subcontracting partnerships, call or write to our head office.")}

  <section class="block">
    <div class="wrap">
      <div class="contact">
        <div class="card">
          <span class="k">Head office</span>
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
  </section>'''
    return page("contact.html", "Contact", "Contact Vaibhav Laxmi Builders (VLB), Dehradun Road, Saharanpur. Phone +91 98370 16102, email info@vlbinfra.com.", body)


if __name__ == "__main__":
    pages = [("index.html", home), ("about.html", about), ("services.html", services), ("contact.html", contact)]
    if SHOW_PROJECTS:
        pages.append(("projects.html", projects))
    else:
        (ROOT / "projects.html").write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=index.html">'
            '<link rel="canonical" href="https://www.vlbinfra.com/"><title>Vaibhav Laxmi Builders</title></head>'
            '<body><p><a href="index.html">Go to the Vaibhav Laxmi Builders home page</a></p></body></html>\n',
            encoding="utf-8")
    for name, fn in pages:
        (ROOT / name).write_text(fn(), encoding="utf-8")
        print("built", name)
