import html
from typing import List
from app.schema.scene_graph import (
    PosterSceneGraph,
    TextLayer,
    VectorShapeLayer,
    ProceduralPatternLayer,
    AssetLayer,
)


class SVGRenderer:
    """
    Deterministic renderer that compiles a PosterSceneGraph into clean,
    standards-compliant SVG markup with razor-sharp vector fidelity.
    """

    def render(self, scene: PosterSceneGraph) -> str:
        width = scene.canvas.width
        height = scene.canvas.height
        bg_color = scene.canvas.background_color

        defs_elements: List[str] = [
            # Drop shadow filter for 3D hero assets
            """
            <filter id="asset-shadow" x="-30%" y="-30%" width="160%" height="160%">
                <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000000" flood-opacity="0.45" />
            </filter>
            """
        ]

        body_elements: List[str] = []

        # Background base
        body_elements.append(
            f'<rect id="base-canvas" width="{width}" height="{height}" fill="{bg_color}" />'
        )

        # Render layers sorted strictly by z-index
        for layer in scene.get_sorted_layers():
            if not layer.visible:
                continue

            if isinstance(layer, ProceduralPatternLayer):
                rendered, pattern_def = self._render_procedural_pattern(layer)
                if pattern_def:
                    defs_elements.append(pattern_def)
                body_elements.append(rendered)

            elif isinstance(layer, VectorShapeLayer):
                body_elements.append(self._render_vector_shape(layer))

            elif isinstance(layer, AssetLayer):
                body_elements.append(self._render_asset_layer(layer))

            elif isinstance(layer, TextLayer):
                body_elements.append(self._render_text_layer(layer))

        defs_block = f"<defs>\n{''.join(defs_elements)}\n</defs>" if defs_elements else ""
        body_block = "\n".join(body_elements)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" 
     viewBox="0 0 {width} {height}" 
     width="{width}" 
     height="{height}" 
     style="background-color: {bg_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
{defs_block}
{body_block}
</svg>"""
        return svg

    def _render_procedural_pattern(self, layer: ProceduralPatternLayer) -> tuple[str, str]:
        pattern_id = f"pattern-{layer.id}"
        pattern_def = ""
        rendered = ""

        if layer.pattern_type == "halftone_dots":
            spacing = layer.spacing
            r = layer.dot_radius
            pattern_def = f"""
            <pattern id="{pattern_id}" width="{spacing}" height="{spacing}" patternUnits="userSpaceOnUse" patternTransform="rotate({layer.angle})">
                <circle cx="{spacing/2}" cy="{spacing/2}" r="{r}" fill="{layer.color}" opacity="{layer.opacity}" />
            </pattern>
            """
            rendered = f'<rect id="{layer.id}" x="{layer.x}" y="{layer.y}" width="{layer.width}" height="{layer.height}" fill="url(#{pattern_id})" />'

        elif layer.pattern_type == "grid_lines":
            spacing = layer.spacing
            pattern_def = f"""
            <pattern id="{pattern_id}" width="{spacing}" height="{spacing}" patternUnits="userSpaceOnUse">
                <path d="M {spacing} 0 L 0 0 0 {spacing}" fill="none" stroke="{layer.color}" stroke-width="0.75" opacity="{layer.opacity}" />
            </pattern>
            """
            rendered = f'<rect id="{layer.id}" x="{layer.x}" y="{layer.y}" width="{layer.width}" height="{layer.height}" fill="url(#{pattern_id})" />'

        return rendered, pattern_def

    def _render_vector_shape(self, layer: VectorShapeLayer) -> str:
        fill_attr = f'fill="{layer.fill}"' if layer.fill else 'fill="none"'
        stroke_attr = f'stroke="{layer.stroke}" stroke-width="{layer.stroke_width}"' if layer.stroke else ""
        opacity_attr = f'opacity="{layer.opacity}"' if layer.opacity < 1.0 else ""
        transform = f'transform="rotate({layer.rotation} {layer.x + layer.width/2} {layer.y + layer.height/2})"' if layer.rotation else ""

        if layer.shape == "rect":
            rx_attr = f'rx="{layer.corner_radius}"' if layer.corner_radius else ""
            return f'<rect id="{layer.id}" x="{layer.x}" y="{layer.y}" width="{layer.width}" height="{layer.height}" {rx_attr} {fill_attr} {stroke_attr} {opacity_attr} {transform} />'

        elif layer.shape == "circle":
            r = min(layer.width, layer.height) / 2
            cx = layer.x + r
            cy = layer.y + r
            return f'<circle id="{layer.id}" cx="{cx}" cy="{cy}" r="{r}" {fill_attr} {stroke_attr} {opacity_attr} />'

        elif layer.shape == "line":
            if layer.points and len(layer.points) >= 2:
                p1, p2 = layer.points[0], layer.points[1]
                return f'<line id="{layer.id}" x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" {stroke_attr} {opacity_attr} />'
            return f'<line id="{layer.id}" x1="{layer.x}" y1="{layer.y}" x2="{layer.x + layer.width}" y2="{layer.y + layer.height}" {stroke_attr} {opacity_attr} />'

        elif layer.shape == "cross":
            # Stylized geometric 'X' shape
            w, h = layer.width, layer.height
            cx, cy = layer.x + w/2, layer.y + h/2
            return f"""<g id="{layer.id}" transform="translate({cx}, {cy}) rotate({layer.rotation or 45}) translate({-cx}, {-cy})">
                <rect x="{layer.x}" y="{cy - 12}" width="{w}" height="24" {fill_attr} />
                <rect x="{cx - 12}" y="{layer.y}" width="24" height="{h}" {fill_attr} />
            </g>"""

        return ""

    def _render_asset_layer(self, layer: AssetLayer) -> str:
        shadow_attr = 'filter="url(#asset-shadow)"' if layer.drop_shadow else ""
        opacity_attr = f'opacity="{layer.opacity}"' if layer.opacity < 1.0 else ""
        transform = f'transform="rotate({layer.rotation} {layer.x + layer.width/2} {layer.y + layer.height/2})"' if layer.rotation else ""

        if layer.asset_path:
            return f'<image id="{layer.id}" href="{layer.asset_path}" x="{layer.x}" y="{layer.y}" width="{layer.width * layer.scale}" height="{layer.height * layer.scale}" {shadow_attr} {opacity_attr} {transform} />'
        
        # Placeholder indicator if asset image is pending generation
        return f"""<g id="{layer.id}" {transform}>
            <rect x="{layer.x}" y="{layer.y}" width="{layer.width}" height="{layer.height}" fill="none" stroke="#FFFFFF" stroke-dasharray="6,6" opacity="0.35" />
            <rect x="{layer.x + 20}" y="{layer.y + layer.height/2 - 25}" width="{layer.width - 40}" height="50" rx="8" fill="#000000" opacity="0.4" />
            <text x="{layer.x + layer.width/2}" y="{layer.y + layer.height/2 + 6}" fill="#FFFFFF" opacity="0.85" font-size="16" font-weight="600" text-anchor="middle">⚡ [Hero 3D Asset Slot: Alpha Cutout]</text>
        </g>"""

    def _render_text_layer(self, layer: TextLayer) -> str:
        escaped_content = html.escape(layer.content)
        style_parts = [
            f"font-family: '{layer.font_family}', sans-serif",
            f"font-size: {layer.font_size}px",
            f"font-weight: {layer.font_weight}",
            f"fill: {layer.color}",
        ]

        if layer.letter_spacing != 0.0:
            style_parts.append(f"letter-spacing: {layer.letter_spacing}px")

        if layer.text_transform != "none":
            style_parts.append(f"text-transform: {layer.text_transform}")

        text_anchor = "start"
        if layer.align == "center":
            text_anchor = "middle"
        elif layer.align == "right":
            text_anchor = "end"

        transform = f'transform="rotate({layer.rotation} {layer.x} {layer.y})"' if layer.rotation else ""
        writing_mode_attr = f'writing-mode="{layer.writing_mode}"' if layer.writing_mode != "horizontal-tb" else ""

        style_str = "; ".join(style_parts)
        return f'<text id="{layer.id}" x="{layer.x}" y="{layer.y}" text-anchor="{text_anchor}" style="{style_str}" {transform} {writing_mode_attr} opacity="{layer.opacity}">{escaped_content}</text>'
