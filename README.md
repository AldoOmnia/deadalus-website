# Daedalus — Landing Page

Scroll-driven landing page for Daedalus, built as a single static `index.html` from the
[Figma design](https://www.figma.com/design/4GwTlarBkzhjqIuQSCYWjT/Logo-Deadalus?node-id=23-47).

## Run

Any static server works:

```bash
python3 -m http.server 8741
# open http://localhost:8741/
```

## How it works

- The whole Desktop 1 → 7 sequence is one sticky stage driven by scroll progress
  (`index.html`, bottom `<script>`): wordmark rises over the brand gradient, morphs into
  the isometric text on the labyrinth logo, the logo docks at the top, and the
  Desktop 5/6/7 copy cross-fades beneath it.
- Layout ratios are derived from the 1440 × 1024 Figma frames; type scales with viewport
  height (`--fs`) so text keeps its proportion to the logo.

## Assets

- `assets/logo.svg` — high-res isometric labyrinth logo (text stripped; rendered live for the morph)
- `assets/connector.svg` — dashed connector diagram for the three pillars
- `assets/factory-brand.png` — factory illustration, gradient-mapped to the brand colors,
  white top fade, black bottom dissolve
- `assets/process_factory.py` — regenerates `factory-brand.png` from `factory-raw1.png`
  (requires Pillow + numpy): `cd assets && python3 process_factory.py`

## Contact

- aaron@deadalusiq.com
- aldo@deadalusiq.com
