import os
import json
import shutil
import subprocess
from app.deconstructor.vibe_extractor import VibeExtractor
from app.planner.layout_planner import LayoutPlanner, UserBrief
from app.renderer.svg_renderer import SVGRenderer

NEW_IMAGE_PATH = "/home/tinchu/.gemini/antigravity/brain/5e749c77-a185-4d88-8183-023bdfea2710/.user_uploaded/media_1792092133387_6b505907.png"
ARTIFACT_DIR = "/home/tinchu/.gemini/antigravity/brain/5e749c77-a185-4d88-8183-023bdfea2710"


def main():
    print("=== Step 1: Deconstructing New Inspo Image ===")
    extractor = VibeExtractor()
    dna = extractor.extract_dna(
        image_path=NEW_IMAGE_PATH,
        user_notes="Livid and baseful vibe, modern geometric Bauhaus, flowing connected organic vector forms and rich color accents"
    )
    print("\n--- Extracted DesignDNA ---")
    print(dna.model_dump_json(indent=2))
    with open("posterlad_dna.json", "w") as f:
        f.write(dna.model_dump_json(indent=2))

    print("\n=== Step 2: Planning Layout with User Brief ===")
    brief = UserBrief(
        headline="The Best Show",
        subtitle="xyz.io",
        date_time="SERIES 2026 • LIVE",
        venue="BROADCAST ONLINE",
        metadata=[
            "A Livid & Baseful Production",
            "curated by xyz.io",
            "www.xyz.io/the-best-show",
            "All Rights Reserved © 2026"
        ],
        custom_hero_prompt=None
    )

    planner = LayoutPlanner()
    scene = planner.plan_poster(dna=dna, brief=brief)
    print(f"\nPlanned Scene Graph with {len(scene.layers)} layers!")
    with open("best_show_scene_graph.json", "w") as f:
        f.write(scene.model_dump_json(indent=2))

    print("\n=== Step 3: Compiling to SVG ===")
    renderer = SVGRenderer()
    svg_code = renderer.render(scene)
    with open("best_show_poster.svg", "w") as f:
        f.write(svg_code)

    print("\n=== Step 4: Rasterizing to PNG ===")
    subprocess.run(["magick", "-background", "none", "best_show_poster.svg", "best_show_poster.png"], check=True)

    if os.path.exists(ARTIFACT_DIR):
        shutil.copy("best_show_poster.png", os.path.join(ARTIFACT_DIR, "best_show_poster.png"))
        shutil.copy("best_show_poster.svg", os.path.join(ARTIFACT_DIR, "best_show_poster.svg"))
        print(f"Copied to artifact directory: {ARTIFACT_DIR}")

    print("\n=== Success! Poster Generated ===")


if __name__ == "__main__":
    main()
