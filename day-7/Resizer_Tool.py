import os
from PIL import Image

def resize_images(image_paths, output_folder, width, height, output_format="JPEG", keep_aspect_ratio=False):
   
    os.makedirs(output_folder, exist_ok=True)

    for input_path in image_paths:
        try:
            with Image.open(input_path) as img:
                if keep_aspect_ratio:
                    img.thumbnail((width, height))  
                else:
                    img = img.resize((width, height))  

                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_path = os.path.join(output_folder, f"{base_name}.{output_format.lower()}")
                img.save(output_path, output_format)
                print(f"Processed: {output_path}")

        except Exception as e:
            print(f"Skipping {input_path}: {e}")

if __name__ == "__main__":
    
    base_dir = os.path.dirname(os.path.abspath(__file__))

    input_folder_name = input("Enter the input folder name: ").strip() or "images"
    input_folder = os.path.join(base_dir, input_folder_name)

    if not os.path.exists(input_folder):
        print(f" Error: Folder '{input_folder}' not found.")
        exit()

    all_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    if not all_files:
        print(" No images found in the folder.")
        exit()

    print("\nAvailable images:")
    for i, filename in enumerate(all_files, start=1):
        print(f"{i}. {filename}")

    choice = input("\nDo you want to process all images? (yes/no): ").strip().lower()

    if choice == "yes":
        selected_paths = [os.path.join(input_folder, f) for f in all_files]
    else:
        selected_indices = input("Enter the image numbers to process (comma separated, e.g., 1,3,5): ").strip()
        selected_indices = [int(x) for x in selected_indices.split(",") if x.strip().isdigit()]
        selected_paths = [os.path.join(input_folder, all_files[i - 1]) for i in selected_indices if 1 <= i <= len(all_files)]

    output_folder_name = input("Enter the output folder name: ").strip() or "resized"
    output_folder = os.path.join(base_dir, output_folder_name)

    width = int(input("Enter the target width in pixels: ").strip())
    height = int(input("Enter the target height in pixels: ").strip())
    output_format = input("Enter the output format (e.g., JPEG, PNG): ").strip().upper()
    aspect_choice = input("Keep aspect ratio? (yes/no): ").strip().lower()

    keep_aspect_ratio = aspect_choice == "yes"

    resize_images(selected_paths, output_folder, width, height, output_format, keep_aspect_ratio)
