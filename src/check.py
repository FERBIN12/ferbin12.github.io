"""Guard: every number and every sentence-ish text run on the 0895299 page must survive on each built page."""
import re, sys
from bs4 import BeautifulSoup, Comment
def text(path):
    s = BeautifulSoup(open(path).read(), "html.parser")
    for t in s(["script", "style", "head"]): t.decompose()
    for c in s.find_all(string=lambda x: isinstance(x, Comment)): c.extract()
    return re.sub(r"\s+", " ", s.get_text(" ")).replace("\xa0", " ")
old = text("src/source_0895299.html")
nums = lambda t: re.findall(r"\d[\d,.]*\d|\d", t)
from collections import Counter
oldn = Counter(nums(old))
_s = BeautifulSoup(open("src/source_0895299.html").read(), "html.parser")
for t in _s(["script", "style", "head"]): t.decompose()
oldsent = set()
for el in _s.find_all(["p", "h1", "h2", "h3", "h4", "dt", "dd", "figcaption", "span", "li", "summary"]):
    t = re.sub(r"\s+", " ", el.get_text(" ")).replace("\xa0", " ").strip()
    if len(t) > 3 and not re.fullmatch(r"\d\d", t): oldsent.add(t)
retired = set(l.strip() for l in open("src/retired_labels.txt") if l.strip() and not l.startswith("#"))
oldsent = {x for x in oldsent if not any(x.startswith(r[:120]) for r in retired)}
oldn.pop("08", None); oldn.pop("09", None)  # section numbers
bad = 0
for p in ["index.html", "sim/index.html", "field/index.html"]:
    new = text(p); newn = Counter(nums(new))
    miss = {n: c for n, c in oldn.items() if newn[n] < 1}
    lost = [x for x in oldsent if x not in new]
    print(p, "numbers missing:", miss or "none", "| sentences missing:", len(lost))
    for x in sorted(lost): print("   -", x[:140])
    bad += len(miss) + len(lost)
sys.exit(1 if bad else 0)
