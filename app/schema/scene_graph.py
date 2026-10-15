from typing import List, Optional, Literal, Union, Annotated
from pydantic import BaseModel, Field


class Canvas(BaseModel):
    width: int = Field(default=1200, description="Canvas width in px (default 3:4 print/digital ratio)")
    height: int = Field(default=1600, description="Canvas height in px")
    background_color: str = Field(default="#002BFF", description="Solid base color hex")
    background_gradient: Optional[str] = Field(
        None, 
        description="Optional CSS gradient string, e.g. linear-gradient(180deg, #002BFF 0%, #001280 100%)"
    )


class BaseLayer(BaseModel):
    id: str
    name: Optional[str] = None
    z_index: int = Field(default=1, description="Stacking order: lower sits in background, higher sits on top")
    opacity: float = Field(default=1.0, ge=0.0, le=1.0)
    visible: bool = True


class TextLayer(BaseLayer):
    type: Literal["text"] = "text"
    content: str
    x: float = Field(description="X position in canvas coordinates")
    y: float = Field(description="Y position in canvas coordinates")
    font_family: str = Field(default="Helvetica Neue")
    font_size: float = Field(default=48.0)
    font_weight: str = Field(default="700", description="'400', '700', 'bold', 'black', etc.")
    color: str = Field(default="#FFFFFF")
    align: Literal["left", "center", "right"] = "left"
    letter_spacing: float = Field(default=0.0, description="Letter tracking in px")
    line_height: float = Field(default=1.1, description="Line height multiplier")
    text_transform: Literal["none", "uppercase", "lowercase", "capitalize"] = "none"
    writing_mode: Literal["horizontal-tb", "vertical-rl"] = "horizontal-tb"
    rotation: float = Field(default=0.0, description="Rotation in degrees")


class VectorShapeLayer(BaseLayer):
    type: Literal["vector_shape"] = "vector_shape"
    shape: Literal["rect", "circle", "line", "cross", "polygon"]
    x: float
    y: float
    width: float
    height: float
    fill: Optional[str] = Field(None, description="Fill color hex or 'none'")
    stroke: Optional[str] = Field(None, description="Stroke color hex or 'none'")
    stroke_width: float = 0.0
    rotation: float = 0.0
    corner_radius: float = 0.0
    # For custom shapes or lines
    points: Optional[List[List[float]]] = Field(None, description="Coordinate pairs for polygon/line")


class ProceduralPatternLayer(BaseLayer):
    type: Literal["procedural_pattern"] = "procedural_pattern"
    pattern_type: Literal["halftone_dots", "wireframe_splines", "grid_lines"]
    x: float
    y: float
    width: float
    height: float
    # Pattern specific controls
    dot_radius: float = 2.5
    spacing: float = 12.0
    angle: float = 45.0
    color: str = "#FFFFFF"


class AssetLayer(BaseLayer):
    """
    Isolated hero centerpiece (3D object, sculpture, or photograph).
    Rendered on a transparent alpha background.
    """
    type: Literal["isolated_asset"] = "isolated_asset"
    prompt: str = Field(description="Prompt that generated this isolated asset")
    asset_path: Optional[str] = Field(None, description="Local path or URL to RGBA PNG")
    x: float
    y: float
    width: float
    height: float
    scale: float = 1.0
    rotation: float = 0.0
    blend_mode: Literal["normal", "multiply", "screen", "overlay"] = "normal"
    drop_shadow: bool = False
    shadow_color: str = "rgba(0, 0, 0, 0.45)"
    shadow_blur: float = 25.0
    shadow_offset_y: float = 15.0


# Discriminated union of all supported layers
LayerType = Annotated[
    Union[TextLayer, VectorShapeLayer, ProceduralPatternLayer, AssetLayer],
    Field(discriminator="type")
]


class PosterSceneGraph(BaseModel):
    title: str = Field(default="Untitled Poster")
    canvas: Canvas = Field(default_factory=Canvas)
    layers: List[LayerType] = Field(default_factory=list)

    def get_sorted_layers(self) -> List[LayerType]:
        """Returns layers ordered strictly by z_index for correct rendering."""
        return sorted(self.layers, key=lambda l: l.z_index)
