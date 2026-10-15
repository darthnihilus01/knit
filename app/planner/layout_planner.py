import os
import json
import httpx
from typing import Optional, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from app.schema.design_dna import DesignDNA
from app.schema.scene_graph import PosterSceneGraph

load_dotenv()


class UserBrief(BaseModel):
    """The content and copy the user wants on the poster."""
    headline: str = Field(description="Main title or festival/event name, e.g. 'SYNTHESIS'")
    subtitle: Optional[str] = Field(None, description="Supporting title or category")
    date_time: Optional[str] = Field(None, description="Event date or time")
    venue: Optional[str] = Field(None, description="Location, city, or club venue")
    metadata: List[str] = Field(
        default_factory=list, 
        description="Extra copy like tickets, curated by, website, or social handles"
    )
    custom_hero_prompt: Optional[str] = Field(
        None, 
        description="Optional custom prompt for the 3D center asset. If omitted, AI invents one matching the vibe."
    )


class LayoutPlanner:
    """
    Acts as the Senior Art Director & Layout Engine.
    Takes a DesignDNA (aesthetic rules) and a UserBrief (text copy)
    and computes a full, structured PosterSceneGraph (AST) with exact coordinates,
    typographic hierarchy, procedural patterns, and layer depths.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://openrouter.ai/api/v1",
        default_model: str = "google/gemini-2.5-flash",
    ):
        self.api_key = (
            api_key
            or os.getenv("OPENROUTER_API_KEY")
            or os.getenv("ANTHROPIC_AUTH_TOKEN")
        )
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is not set.")

        self.base_url = base_url.rstrip("/")
        self.default_model = default_model

    def plan_poster(
        self,
        dna: DesignDNA,
        brief: UserBrief,
        model: Optional[str] = None,
    ) -> PosterSceneGraph:
        """
        Translates aesthetic rules + copy into a concrete, mathematically balanced PosterSceneGraph.
        """
        target_model = model or self.default_model
        schema_json = json.dumps(PosterSceneGraph.model_json_schema(), indent=2)

        system_prompt = (
            "You are a World-Class Graphic Designer, Typography Master, and Creative Director.\n"
            "Your job is to generate a complete, mathematically balanced 'PosterSceneGraph' (AST) in JSON.\n\n"
            "CANVAS SPECIFICATIONS:\n"
            "- Dimensions: 1200 width × 1600 height (Aspect Ratio 3:4).\n"
            "- Coordinate system: (0,0) is top-left, (1200, 1600) is bottom-right.\n\n"
            "COMPOSITIONAL RULES FOR HIGH-END HUMAN DESIGN (NO AI SLOP):\n"
            "1. Margins & Safe Zones: Keep a 100px to 140px margin from canvas borders for main content.\n"
            "2. Adapt to Design Genre:\n"
            "   - If has_isolated_3d_subject is False (Geometric / Bauhaus / PosterLad / Swiss vector):\n"
            "     * Do NOT add an AssetLayer.\n"
            "     * Create a bold, rhythmic visual composition across the upper 80% of canvas with 6-12 solid vector shapes (circles of varying radii 50-250px, connected rect bars, wave splines) using all palette colors (primary, secondary, accent, extra_colors) at full opacity (0.85-1.0)!\n"
            "     * Place the typography in a crisp, multi-column bottom footer (y: 1450 to 1520), or elegant top/bottom split.\n"
            "   - If has_isolated_3d_subject is True (Contemporary 3D / Surrealism):\n"
            "     * Include a central AssetLayer (z_index=3) with detailed 3D prompt and drop_shadow=true.\n"
            "     * Add foreground geometric accents (z_index=4-5) that slice in front to create depth.\n"
            "3. Typographic Scale & Hierarchy:\n"
            "   - Headline: 64px to 100px (or 40-56px if in a footer block), bold/black weight, high contrast.\n"
            "   - Subtitle: 24px to 36px, medium/bold weight.\n"
            "   - Metadata/Dates/Credits: 14px to 20px, crisp, letter-spacing (0.5 to 2.0px).\n"
            "4. Color Discipline: Use ONLY colors from the provided DesignDNA palette (background, primary, secondary, accent, extra_colors).\n\n"
            "CRITICAL REQUIREMENT: Output MUST be valid, complete JSON conforming EXACTLY to this JSON Schema:\n"
            f"{schema_json}\n\n"
            "Do NOT wrap with commentary. Output raw JSON only."
        )

        user_prompt = f"""
DESIGN DNA (Aesthetic Rules):
{dna.model_dump_json(indent=2)}

USER CONTENT BRIEF:
{brief.model_dump_json(indent=2)}

Synthesize these into a cohesive, professional PosterSceneGraph JSON.
"""

        payload = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 3500,
            "response_format": {"type": "json_object"},
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://knit-poster-engine.local",
            "X-Title": "Knit Poster Engine",
        }

        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"OpenRouter API call failed (HTTP {response.status_code}): {response.text}"
            )

        resp_json = response.json()
        raw_content = resp_json["choices"][0]["message"]["content"].strip()

        if raw_content.startswith("```"):
            raw_content = raw_content.split("```")[1]
            if raw_content.startswith("json"):
                raw_content = raw_content[4:]
        raw_content = raw_content.strip()

        parsed_data = json.loads(raw_content)
        return PosterSceneGraph.model_validate(parsed_data)
