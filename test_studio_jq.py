from app.schema.scene_graph import (
    PosterSceneGraph,
    Canvas,
    TextLayer,
    VectorShapeLayer,
    ProceduralPatternLayer,
    AssetLayer,
)
from app.renderer.svg_renderer import SVGRenderer


def create_studio_jq_mock() -> PosterSceneGraph:
    """
    Recreates the structural layout of the Studio JQ 'Poster 76'
    using our clean PosterSceneGraph schema.
    """
    scene = PosterSceneGraph(
        title="Studio JQ - Poster 76 Replica",
        canvas=Canvas(
            width=1200,
            height=1600,
            background_color="#002BFF",  # Electric Klein Blue
        ),
        layers=[
            # 1. Background Halftone Matrix (Top-Right zone)
            ProceduralPatternLayer(
                id="bg-halftone-top",
                name="Top Halftone Dot Grid",
                pattern_type="halftone_dots",
                x=650,
                y=40,
                width=500,
                height=300,
                dot_radius=3.0,
                spacing=16.0,
                angle=45.0,
                color="#FFFFFF",
                opacity=0.75,
                z_index=1,
            ),
            # 2. Background Halftone Matrix (Bottom-Center zone)
            ProceduralPatternLayer(
                id="bg-halftone-bottom",
                name="Bottom Halftone Dot Grid",
                pattern_type="halftone_dots",
                x=320,
                y=1100,
                width=350,
                height=450,
                dot_radius=3.0,
                spacing=16.0,
                angle=45.0,
                color="#FFFFFF",
                opacity=0.75,
                z_index=1,
            ),
            # 3. Ambient 3D Fluid Gradient (Behind Hero)
            VectorShapeLayer(
                id="ambient-gradient-blob",
                name="Soft Organic Gradient Background",
                shape="rect",
                x=220,
                y=120,
                width=760,
                height=1250,
                fill="#FF8CA3",
                corner_radius=380,
                opacity=0.35,
                z_index=2,
            ),
            # 4. Hero 3D Centerpiece: Sliced Ribbon Torso (Isolated Asset)
            AssetLayer(
                id="hero-sliced-man",
                name="Hero 3D Sliced Ribbon Torso",
                prompt="3D surreal sculpture of a human torso sliced into floating spiral ribbons, textured paper material, dramatic studio lighting, transparent background",
                x=340,
                y=200,
                width=520,
                height=900,
                drop_shadow=True,
                shadow_blur=30.0,
                shadow_offset_y=20.0,
                z_index=3,
            ),
            # 5. Overlapping Geometric Crossbar (Intersects chest)
            VectorShapeLayer(
                id="crossbar-rect",
                name="Horizontal Pastel Crossbar",
                shape="rect",
                x=420,
                y=680,
                width=500,
                height=32,
                fill="#F3F0EC",
                corner_radius=4,
                z_index=4,  # IN FRONT of the 3D hero torso!
            ),
            # 6. Overlapping White Circle (Intersects lower body)
            VectorShapeLayer(
                id="white-circle-focal",
                name="Solid White Circle Accent",
                shape="circle",
                x=640,
                y=1030,
                width=130,
                height=130,
                fill="#FFFFFF",
                z_index=4,  # IN FRONT of the legs
            ),
            # 7. Geometric White Cross 'X' (Right Margin Anchor)
            VectorShapeLayer(
                id="white-cross-x",
                name="Right Margin Cross Anchor",
                shape="cross",
                x=880,
                y=750,
                width=240,
                height=240,
                fill="#FFFFFF",
                z_index=4,
            ),
            # --- TYPOGRAPHY LAYERS (100% Vector & Clean) ---
            # Top-Left: Metadata / Instagram
            TextLayer(
                id="text-instagram-label",
                content="+ instagram:",
                x=120,
                y=140,
                font_size=18,
                font_weight="500",
                color="#FFFFFF",
                letter_spacing=1.0,
                z_index=10,
            ),
            TextLayer(
                id="text-instagram-handle",
                content="@madebystudiojq",
                x=120,
                y=168,
                font_size=22,
                font_weight="700",
                color="#FFFFFF",
                letter_spacing=0.5,
                z_index=10,
            ),
            # Top-Right: Collection & 2018
            TextLayer(
                id="text-collection-label",
                content="Collection",
                x=980,
                y=180,
                font_size=18,
                font_weight="600",
                color="#FFFFFF",
                writing_mode="vertical-rl",
                z_index=10,
            ),
            TextLayer(
                id="text-year-2018",
                content="2018",
                x=1040,
                y=160,
                font_size=64,
                font_weight="900",
                color="#FFFFFF",
                line_height=0.9,
                z_index=10,
            ),
            # Bottom-Left: Poster 76
            TextLayer(
                id="text-poster-label",
                content="Poster",
                x=120,
                y=1380,
                font_size=20,
                font_weight="600",
                color="#FFFFFF",
                z_index=10,
            ),
            VectorShapeLayer(
                id="poster-rule-line",
                shape="line",
                x=190,
                y=1374,
                width=60,
                height=0,
                stroke="#FFFFFF",
                stroke_width=2.5,
                z_index=10,
            ),
            TextLayer(
                id="text-poster-number",
                content="76",
                x=120,
                y=1460,
                font_size=72,
                font_weight="900",
                color="#FFFFFF",
                z_index=10,
            ),
            # Bottom-Right: S&G Brand + Vertical Copyright
            TextLayer(
                id="text-sg-brand",
                content="S&G",
                x=1080,
                y=1460,
                align="right",
                font_size=56,
                font_weight="900",
                color="#FFFFFF",
                z_index=10,
            ),
            TextLayer(
                id="text-copyright-vertical",
                content="Jonathan Quintin Copyrighted © 2018",
                x=1065,
                y=1220,
                font_size=15,
                font_weight="500",
                color="#FFFFFF",
                writing_mode="vertical-rl",
                opacity=0.85,
                z_index=10,
            ),
        ],
    )
    return scene


if __name__ == "__main__":
    scene = create_studio_jq_mock()
    renderer = SVGRenderer()
    svg_output = renderer.render(scene)

    with open("studio_jq_mock.svg", "w") as f:
        f.write(svg_output)

    print("Successfully generated studio_jq_mock.svg!")
