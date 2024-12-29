import json
import os
from pathlib import Path
from difflib import SequenceMatcher

def find_most_similar_filename(target, file_list):
    """Find the most similar filename from a list using sequence matcher."""
    max_ratio = 0
    best_match = None
    
    for filename in file_list:
        # Compare without extensions
        base_target = os.path.splitext(target)[0]
        base_filename = os.path.splitext(filename)[0]
        
        ratio = SequenceMatcher(None, base_target.lower(), base_filename.lower()).ratio()
        if ratio > max_ratio:
            max_ratio = ratio
            best_match = filename
    
    return best_match if max_ratio > 0.6 else None

def update_card_images():
    # Get all image files from images directory
    images_dir = Path("images")
    image_files = [f.name for f in images_dir.glob("*.webp")]
    
    # Process each JSON file in cards directory
    cards_dir = Path("cards")
    for json_file in cards_dir.glob("*.json"):
        try:
            # Read JSON with UTF-8 encoding
            with open(json_file, 'r', encoding='utf-8') as f:
                card_data = json.load(f)
            
            if "image" in card_data:
                # Get current image filename
                current_image = os.path.basename(card_data["image"])
                base_name = os.path.splitext(current_image)[0]
                webp_name = f"{base_name}.webp"
                
                # Check if exact match exists
                if webp_name in image_files:
                    card_data["image"] = f"image/{webp_name}"
                else:
                    # Find similar filename
                    similar_image = find_most_similar_filename(base_name, image_files)
                    if similar_image:
                        card_data["image"] = f"images/{similar_image}"
                    else:
                        print(f"No matching image found for {current_image}, {json_file}")
                
                # Write JSON with UTF-8 encoding and ensure_ascii=False
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(card_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")

if __name__ == "__main__":
    update_card_images()