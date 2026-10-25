"""One-time: pull every content block out of the 0895299 page into src/content.json, verbatim."""
import json, re
from bs4 import BeautifulSoup, Comment
s = BeautifulSoup(open(__import__("sys").argv[1] if len(__import__("sys").argv)>1 else "index.html").read(), "html.parser")
for c in s.find_all(string=lambda t: isinstance(t, Comment)): c.extract()
inner = lambda el: "".join(str(x) for x in el.contents).strip() if el else ""
txt = lambda el: el.get_text(" ", strip=True) if el else ""

def morph(a):
    v = a.find("video"); src = v.find("source")["src"] if v else None
    med = a.select_one(".morph-media")
    return {"tag": txt(a.select_one(".morph-tag")), "video": src, "poster": v.get("poster") if v else None,
            "aria": v.get("aria-label") if v else "", "wide": "wide" in (med.get("class") or []),
            "title": txt(a.find("h3")),
            "body": "".join(str(p) for p in a.select(".morph-body p:not(.morph-stack)")),
            "stack": inner(a.select_one(".morph-stack"))}

def proj(a):
    v = a.select_one(".proj-media video"); fig = a.select_one(".proj-media")
    badge = a.select_one(".proj-idx b")
    idx = a.select_one(".proj-idx")
    if badge: badge = {"cls": [c for c in badge["class"] if c != "own"][0], "text": txt(badge)}
    idx_text = "".join(str(x) for x in idx.contents if getattr(x, "name", None) != "b").strip()
    return {"idx": idx_text, "badge": badge, "title": txt(a.find("h3")), "meta": inner(a.select_one(".proj-meta")),
            "figure": str(fig) if fig else "", "video": v.find("source")["src"] if v else None,
            "poster": v.get("poster") if v else None, "text": inner(a.select_one(".proj-text")),
            "inst": inner(a.select_one("dl.inst")), "stack": inner(a.select_one(".proj-stack")),
            "extra": "".join(str(x) for x in a.select(":scope > .strip"))}

out = {}
hw = s.find(id="hardware"); out["hardware"] = {"lede": inner(hw.select_one(".field-lede")), "items": [morph(a) for a in hw.select("article.morph")]}
sim = s.find(id="sim"); out["sim"] = [proj(a) for a in sim.select("article.proj")]
pl = s.find(id="platforms"); out["platforms"] = [morph(a) for a in pl.select("article.morph")]
w = s.find(id="work")
out["coop"] = {"lede": inner(w.select_one(".coop-lede")), "roles": inner(w.select_one(".coop-roles")),
               "items": [proj(a) for a in w.select("article.proj")]}
f = s.find(id="field")
out["field"] = {"lede": inner(f.select_one(".field-lede")),
                "cards": [{"k": txt(c.select_one(".field-k")), "v": txt(c.select_one(".field-v")), "p": inner(c.find("p"))} for c in f.select(".field-card")]}
pr = s.find(id="projects")
out["tiles"] = [{"href": t.get("href"), "title": txt(t.find("h4")), "body": "".join(str(p) for p in t.select("p:not(.tile-tags)")),
                 "tags": inner(t.select_one(".tile-tags"))} for t in pr.select(".tiles > .tile")]
pubs = pr.find("h2", string=re.compile("Publications")).find_parent(class_="sec-head").find_next_sibling()
out["pubs_html"] = str(pubs)
ex = s.find(id="experience"); out["experience_html"] = inner(ex.select_one(".xp")) if ex.select_one(".xp") else inner(ex.select_one(".wrap"))
ab = s.find(id="about"); out["about_text"] = inner(ab.select_one(".about-text"))
out["skills_html"] = "".join(str(g) for g in ab.select(".skill-group"))
co = s.find(id="contact"); out["contact_html"] = inner(co.select_one(".contact-grid"))
out["bench"] = str(hw.select_one(".bench-strip"))
out["head_meta"] = str(s.find("head"))
json.dump(out, open("src/content.json", "w"), indent=1, ensure_ascii=False)
print({k: (len(v) if isinstance(v, (list, dict)) else len(v)) for k, v in out.items()})
print([i["title"][:30] for i in out["coop"]["items"]], len(out["tiles"]), [c["k"] for c in out["field"]["cards"]])
