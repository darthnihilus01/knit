# Knit 🧶

> **A human-grade poster design engine powered by aesthetic deconstruction and deterministic vector layouts.**

Knit is an AI graphic design engine built specifically to solve the "AI Slop" problem. Instead of generating flat, over-rendered, halluncinated JPEGs with illegible text, Knit operates like a modern digital design studio:

1. **Aesthetic Deconstructor (VLM):** Analyzes inspiration images/moodboards and extracts a pure **Design DNA** (palette, grid system, typographic rules, negative space ratios).
2. **Layout & Scene Graph Planner (LLM):** Plans an Abstract Syntax Tree (`PosterSceneGraph`) of layers, bounding boxes, z-index hierarchy, and typographic styling.
3. **Dual-Track Synthesis:**
   - **Isolated AI Assets:** Only used for 3D/photographic centerpieces with alpha transparency.
   - **Procedural Vectors:** Pure mathematical halftones, wireframe splines, and geometric shapes.
   - **Deterministic Typography:** Real OpenType fonts, exact tracking, and CSS transforms (e.g. vertical rotated edge text).
4. **Deterministic SVG Compiler:** Outputs razor-sharp, print-ready, 100% editable SVG layouts.

---

## Architecture

```
User Inspo Image + Brief
          │
          ▼
[VibeExtractor (VLM)] ──────► DesignDNA (JSON)
                                   │
                                   ▼
                       [LayoutPlanner (LLM)]
                                   │
                                   ▼
                          PosterSceneGraph (AST)
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
          [Isolated AI Asset]           [Vector & Font Engine]
                    │                             │
                    └──────────────┬──────────────┘
                                   ▼
                         [SVGRenderer Compiler]
                                   │
                                   ▼
                       Clean, Editable SVG Poster
```

---

## Quickstart

### 1. Setup Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Keys
Copy `.env.example` to `.env` and provide your OpenRouter key:
```bash
OPENROUTER_API_KEY=your_key_here
```

### 3. Run the Studio JQ Replica Test
```bash
python test_studio_jq.py
```
This compiles `studio_jq_mock.svg` directly from the `PosterSceneGraph` AST.

---

## Project Structure

```
knit/
├── app/
│   ├── schema/              # Central AST & DesignDNA Pydantic definitions
│   │   ├── design_dna.py    # Palette, typography rules, grid definitions
│   │   └── scene_graph.py   # Canvas, Text, Vector, Procedural, and Asset layers
│   ├── deconstructor/       # VLM-powered vibe extraction from inspo images
│   │   └── vibe_extractor.py
│   ├── planner/             # Layout & hierarchy scene graph solver
│   ├── generators/          # Procedural patterns & isolated diffusion assets
│   └── renderer/            # Deterministic SVG and canvas compilers
│       └── svg_renderer.py
├── test_studio_jq.py        # Studio JQ replica test
└── test_extract_dna.py      # Live VLM deconstruction test
```
