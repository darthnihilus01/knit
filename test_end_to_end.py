import json
import os
import shutil
import subprocess
from app.schema.design_dna import DesignDNA
from app.planner.layout_planner import LayoutPlanner, UserBrief
from app.renderer.svg_renderer import SVGRenderer

ARTIFACT_DIR = "/home/tinchu/.gemini/antigravity/brain/5e749c77-a185-4d88-8183-023bdfea2710"


def main():
    print("--- 1. Loading Extracted Design DNA ---")
    with open("extracted_dna.json", "r") as f:
        dna_data = json.load(f)
    dna = DesignDNA.model_validate(dna_data)
    print(f"Loaded DNA: Genre='{dna.aesthetic_genre}', Base Color={dna.palette.background}")

    print("\n--- 2. Setting Event Brief ---")
    brief = UserBrief(
        headline="SYNTHESIS",
        subtitle="Berlin Electronic Sound & Arts",
        date_time="NOV 24 • 2026",
        venue="KRAFTWERK BERLIN",
        metadata=[
            "+ instagram: @synthesis_berlin",
            "Curated by Studio Echo",
            "Tickets: residentadvisor.net/synthesis",
            "Collection 04 / Edition 2026",
            "All Rights Reserved © 2026"
        ]
    )
    print(f"Brief: Headline='{brief.headline}', Venue='{brief.venue}'")

    print("\n--- 3. Planning Layout via LLM Art Director ---")
    planner = LayoutPlanner()
    scene = planner.plan_poster(dna=dna, brief=brief)
    print(f"Generated Scene Graph with {len(scene.layers)} layers!")

    # Save Scene Graph JSON
    with open("generated_scene_graph.json", "w") as f:
        f.write(scene.model_dump_json(indent=2))
    print("Saved generated_scene_graph.json")

    print("\n--- 4. Compiling to SVG via SVGRenderer ---")
    renderer = SVGRenderer()
    svg_code = renderer.render(scene)

    with open("generated_poster.svg", "w") as f:
        f.write(svg_code)
    print("Saved generated_poster.svg")

    print("\n--- 5. Rasterizing to PNG ---")
    subprocess.run(["magick", "-background", "none", "generated_poster.svg", "generated_poster.png"], check=True)
    print("Saved generated_poster.png")

    # Copy to artifacts directory for inline preview
    if os.path.exists(ARTIFACT_DIR):
        shutil.copy("generated_poster.png", os.path.join(ARTIFACT_DIR, "generated_poster.png"))
        shutil.copy("generated_poster.svg", os.path.join(ARTIFACT_DIR, "generated_poster.svg"))
        print(f"Copied outputs to artifact dir: {ARTIFACT_DIR}")

    print("\nDONE! Poster generation completed successfully.")


if __name__ == "__main__":
    main()
