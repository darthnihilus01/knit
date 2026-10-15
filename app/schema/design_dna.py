from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class ColorPalette(BaseModel):
    background: str = Field(description="Dominant canvas background hex code, e.g. #002BFF")
    primary: str = Field(description="Primary high-contrast color for main titles, e.g. #FFFFFF")
    secondary: str = Field(description="Secondary color for subtitles and structural shapes")
    accent: Optional[str] = Field(None, description="Accent color for highlights or focal points")
    extra_colors: List[str] = Field(default_factory=list, description="Additional spot colors or gradient stops")


class TypographyRule(BaseModel):
    category: Literal["hero_display", "section_header", "metadata_small", "editorial_body"]
    font_family: str = Field(default="Helvetica Neue", description="Clean sans-serif, editorial serif, or geometric font")
    suggested_weight: Literal["light", "normal", "medium", "bold", "black"] = "bold"
    suggested_case: Literal["uppercase", "lowercase", "titlecase", "none"] = "none"
    tracking: float = Field(default=0.0, description="Letter spacing in em or px")


class DesignDNA(BaseModel):
    """
    Extracted aesthetic blueprint from inspiration images.
    Represents the soul/vibe of the design without being tied to specific content.
    """
    aesthetic_genre: str = Field(
        description="e.g. 'Neo-Brutalist Swiss', 'Cybernetic Editorial', 'Vintage Risograph', '3D Bauhaus'"
    )
    vibe_keywords: List[str] = Field(
        default_factory=list,
        description="Key terms describing the atmosphere, e.g. ['stark', 'electric', 'surreal', 'clinical']"
    )
    palette: ColorPalette
    negative_space_ratio: float = Field(
        default=0.45,
        ge=0.0,
        le=1.0,
        description="Target proportion of uncluttered canvas (0.0 = busy/dense, 0.8 = ultra-minimal)"
    )
    grid_system: Literal["12_col_swiss", "asymmetric_split", "centered_focal", "editorial_columns"] = "12_col_swiss"
    typography_rules: List[TypographyRule] = Field(default_factory=list)
    has_isolated_3d_subject: bool = Field(
        default=False,
        description="Whether the design features an isolated volumetric or photographic centerpiece"
    )
    suggested_procedural_patterns: List[Literal["halftone_dots", "wireframe_splines", "grid_lines", "none"]] = Field(
        default_factory=list
    )
