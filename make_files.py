import json
import os
from pathlib import Path

def combine_json_files():
    # Create paths
    cards_folder = Path('cards')
    public_folder = Path('public')
    output_file = public_folder / 'cards.json'

    # Create public folder if it doesn't exist
    public_folder.mkdir(exist_ok=True)

    # Initialize the combined data structure
    combined_data = {"cards": []}

    # Read all JSON files in the cars folder
    for json_file in cards_folder.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Assuming each file contains a single card object
                combined_data["cards"].append(data)
        except json.JSONDecodeError as e:
            print(f"Error reading {json_file}: {e}")
        except Exception as e:
            print(f"Unexpected error with {json_file}: {e}")

    # Write the combined data to cards.json
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully created {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

def copy_image_files():
    # Create paths
    images_folder = Path('images')
    output_folder = Path('public/image')
    
    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Copy all image files
    for image_file in images_folder.glob('*'):
        if image_file.suffix.lower() in ['.webp', '.jpg', '.png', '.gif']:
            try:
                output_path = output_folder / image_file.name
                output_path.write_bytes(image_file.read_bytes())
                print(f"Copied {image_file.name}")
            except Exception as e:
                print(f"Error copying {image_file}: {e}")

if __name__ == "__main__":
    combine_json_files()
    copy_image_files()