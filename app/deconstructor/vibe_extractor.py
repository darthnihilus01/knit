import os
import json
import base64
import httpx
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from app.schema.design_dna import DesignDNA

load_dotenv()


class VibeExtractor:
    """
    Deconstructs an inspiration image into structured DesignDNA using a VLM.
    Acts as an elite Art Director analyzing composition, color palettes,
    typographic hierarchy, and procedural elements.
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
            raise ValueError("OPENROUTER_API_KEY is not set in environment or .env file.")

        self.base_url = base_url.rstrip("/")
        self.default_model = default_model

    def _encode_image(self, image_path: str) -> tuple[str, str]:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found at {image_path}")

        mime_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return encoded, mime_type

    def extract_dna(
        self,
        image_path: str,
        user_notes: Optional[str] = None,
        model: Optional[str] = None,
    ) -> DesignDNA:
        """
        Analyzes the reference image and returns a validated DesignDNA object.
        """
        target_model = model or self.default_model
        b64_data, mime_type = self._encode_image(image_path)

        schema_json = json.dumps(DesignDNA.model_json_schema(), indent=2)

        system_prompt = (
            "You are an elite Senior Art Director and Graphic Design System Architect.\n"
            "Your task is to deconstruct an inspiration poster image into structured 'DesignDNA'.\n"
            "You do NOT copy the text content or exact artwork. Instead, you extract the underlying DESIGN SYSTEM:\n"
            "1. Color Palette: Exact dominant background hex, primary high-contrast text color, secondary, accent.\n"
            "2. Grid & Composition: Swiss 12-col, asymmetric split, centered focal, or editorial.\n"
            "3. Negative Space: Exact ratio of uncluttered canvas (0.1 = dense/busy, 0.7 = minimal/spacious).\n"
            "4. Typography Rules: Detect font moods, weights, letter-spacing, and casing styles.\n"
            "5. Hero Subject: Is there a 3D surreal sculpture, chiseled object, or photo cutout?\n"
            "6. Procedural Patterns: Halftone dot matrices, topographic wireframe contours, grid lines, or none.\n\n"
            "CRITICAL REQUIREMENT: Output MUST be valid, complete, parseable JSON conforming EXACTLY to this JSON Schema:\n"
            f"{schema_json}\n\n"
            "Keep your response concise. Do not exceed 4 typography rules. No commentary outside the JSON."
        )

        user_content = [
            {
                "type": "text",
                "text": "Deconstruct this poster's design system into the DesignDNA JSON format."
                + (f" Context/Vibe notes: {user_notes}" if user_notes else ""),
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{b64_data}"
                },
            },
        ]

        payload = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "temperature": 0.2,
            "max_tokens": 4000,
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
        choice = resp_json["choices"][0]
        raw_content = choice["message"]["content"].strip()
        finish_reason = choice.get("finish_reason")

        if finish_reason == "length":
            print("WARNING: Model response was truncated by max_tokens limit!")

        # Clean markdown code fences if present
        if raw_content.startswith("```"):
            parts = raw_content.split("```")
            if len(parts) >= 2:
                raw_content = parts[1]
                if raw_content.startswith("json"):
                    raw_content = raw_content[4:]
        raw_content = raw_content.strip()

        try:
            parsed_data = json.loads(raw_content)
        except json.JSONDecodeError as e:
            print("FAILED TO PARSE RAW JSON. First 500 chars:")
            print(raw_content[:500])
            print("Last 500 chars:")
            print(raw_content[-500:])
            raise e

        return DesignDNA.model_validate(parsed_data)
