# Building the portfolio

One content source, three entry pages:

| Page | For |
|---|---|
| `/` | robotics software (default) |
| `/sim/` | simulation, robot learning, digital-twin roles |
| `/field/` | FDE, deployment, field and integration roles |

- `content.json`: every writeup, clip, figure and repo tile (copied verbatim from the 0895299 page). Edit text here.
- `site.json`: hero lines, proof tiles, featured cards, repo groups, awards, and each page's order.
- `template.html`: the page layout. `../site.css`, `../main.js`: style and behaviour.

```
python3 src/build.py     # writes index.html, sim/index.html, field/index.html
python3 src/check.py     # fails if any number or text block from the old page went missing
```

Facts are identical on all three pages; only order and emphasis change. `/sim` and `/field` point their canonical URL at `/`.
