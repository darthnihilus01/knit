import json
from app.deconstructor.vibe_extractor import VibeExtractor

IMAGE_PATH = "/home/tinchu/.gemini/antigravity/brain/5e749c77-a185-4d88-8183-023bdfea2710/.user_uploaded/media_1792037740249_c6b90f6f.png"

def main():
    print(f"Connecting to VLM to deconstruct: {IMAGE_PATH}...")
    extractor = VibeExtractor()
    
    # We can try gemini-2.0-flash-001 or any vision model supported on OpenRouter
    dna = extractor.extract_dna(
        image_path=IMAGE_PATH,
        user_notes="Contemporary graphic design poster with 3D sculpture and Swiss typography"
    )

    print("\nSuccessfully extracted DesignDNA!")
    print(json.dumps(dna.model_dump(), indent=2))

    with open("extracted_dna.json", "w") as f:
        f.write(json.dumps(dna.model_dump(), indent=2))
    print("\nSaved result to extracted_dna.json")

if __name__ == "__main__":
    main()
