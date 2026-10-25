"""Build the portfolio: one content source -> index.html, sim/index.html, field/index.html.
content.json = verbatim blocks from the 0895299 page (edit here); site.json = hero, proof, cards, variant order."""
import json, re, os
from pathlib import Path
import jinja2
ROOT = Path(__file__).resolve().parent.parent
c = json.load(open(ROOT / "src/content.json"))
site = json.load(open(ROOT / "src/site.json"))

for h in c["hardware"]["items"]:
    h["poster_auto"] = h["poster"] or "assets/img/real/" + Path(h["video"]).stem + "_poster.jpg"
for key, f in site["featured"].items():
    src = f.get("from", "")
    if src.startswith("sim:"):
        a = c["sim"][int(src[4:])]
        f.update(video=a["video"], poster=a["poster"], full=a,
                 aria=re.search(r'aria-label="([^"]*)"', a["figure"]).group(1),
                 caption=(re.search(r"<figcaption>(.*?)</figcaption>", a["figure"], re.S) or [None, ""])[1].strip())
tiles = {t["title"]: t for t in c["tiles"]}
used = [t for g in site["oss_groups"] for t in g[1]]
assert sorted(used) == sorted(tiles), set(tiles) ^ set(used)

ROLE = {"index": "Robotics Software Engineer", "sim": "Robotics Simulation Engineer", "field": "Robotics Field & Deployment Engineer"}
NAV = {"work": "Work", "hardware": "Hardware", "range": "Simulation", "experience": "Experience", "oss": "Open source", "contact": "Contact"}
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
env = jinja2.Environment(loader=jinja2.FileSystemLoader(ROOT / "src"), autoescape=False, trim_blocks=True, lstrip_blocks=True)
env.filters["slug"] = slug
tpl = env.get_template("template.html")

def rebase(html, b):
    return re.sub(r'(src|poster|href)="assets/', lambda m: f'{m.group(1)}="{b}assets/', html) if b else html

for name, v in site["variants"].items():
    v = dict(v, title_role=ROLE[name])
    plain = re.sub(r"<[^>]+>|&[a-z]+;", " ", v["sub"])
    v["meta_desc"] = re.sub(r"\s+", " ", plain).strip()[:300]
    v["og_desc"] = v["meta_desc"][:200]
    b = "../" * v["path"].count("/")
    html = tpl.render(v=v, site=site, c=c, b=b, tiles=tiles, navnames=NAV)
    html = rebase(html, b)
    out = ROOT / v["path"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT), len(html) // 1024, "KB")
