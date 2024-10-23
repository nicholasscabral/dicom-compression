import os
import numpy as np
import pydicom
from PIL import Image
from write_result_csv import update_mse_csv  # Import the CSV update function


def calculate_mse(original_image, compressed_image):
    mse = np.mean((original_image - compressed_image) ** 2)
    return round(mse, 2)  # Round to two decimal places


def normalize_image(image):
    return ((image - np.min(image)) / (np.max(image) - np.min(image)) * 255).astype(
        np.uint8
    )


def read_dicom_image(path):
    ds = pydicom.dcmread(path)
    return normalize_image(ds.pixel_array.astype(np.float32))


def read_image(path, is_pca=False):
    if is_pca:
        data = np.load(path)
        compressed_image = data["compressed_image"]
        principal_components = data["principal_components"]
        mean = data["mean"]
        reconstructed_image = np.dot(compressed_image, principal_components) + mean
        return normalize_image(reconstructed_image)
    else:
        return np.array(Image.open(path).convert("L"), dtype=np.uint8)


def process_images(original_directory, compressed_directories, compressed_extensions):
    results = []  # Collect results here
    for file in os.listdir(original_directory):
        if not file.endswith(".dcm"):
            continue

        original_image = read_dicom_image(os.path.join(original_directory, file))

        for method, directory in compressed_directories.items():
            compressed_file = os.path.splitext(file)[0] + compressed_extensions[method]
            compressed_path = os.path.join(directory, compressed_file)

            if not os.path.exists(compressed_path):
                print(f"File not found: {compressed_path}")
                continue

            compressed_image = read_image(
                compressed_path, is_pca=(method.startswith("pca"))
            )
            if compressed_image.shape != original_image.shape:
                print(f"Size mismatch for {file} in method {method}")
                continue

            mse = calculate_mse(original_image, compressed_image)

            # Build the method name
            pca_method_mapping = {
                "pca95": "PCA-950",
                "pca975": "PCA-975",
                "pca99": "PCA-990",
            }

            # Dentro do loop:
            if method.startswith("pca"):
                method_name = pca_method_mapping.get(method, f"PCA-{method[3:]}")
            else:
                method_name = method.upper()

            # Call the CSV update function to add MSE
            update_mse_csv(
                f"{os.path.basename(original_directory)}/{file}", method_name, mse
            )

            print(
                f"MSE for {os.path.basename(original_directory)}/{file} in method {method}: {mse}"
            )

            # Collect the result
            results.append(
                {
                    "file": f"{os.path.basename(original_directory)}/{file}",
                    "method": method_name,
                    "mse": mse,
                }
            )

    return results


# Directories of the original and compressed images
original_directories = {
    "lung": "/media/nicholas/files/tcc-cancer-images/lung-512x512",
    "breast": "/media/nicholas/files/tcc-cancer-images/breast-512x512",
    "brain": "/media/nicholas/files/tcc-cancer-images/brain-512x512",
}

compressed_directories_base = {
    "png": "-png-compressed",
    "jpeg": "-jpeg-compressed",
    "pca95": "-pca-compressed-950",
    "pca975": "-pca-compressed-975",
    "pca99": "-pca-compressed-990",
}

compressed_extensions = {
    "png": ".png",
    "jpeg": ".jpeg",
    "pca95": ".npz",
    "pca975": ".npz",
    "pca99": ".npz",
}

all_results = []

# Process images for each category
for category in original_directories:
    print(f"Processing {category} images...")
    compressed_directories = {
        method: original_directories[category] + compressed_directories_base[method]
        for method in compressed_directories_base
    }
    category_results = process_images(
        original_directories[category], compressed_directories, compressed_extensions
    )
    all_results.extend(category_results)

# At the end, write all results to a txt file
with open("mse_results.txt", "w") as f:
    for result in all_results:
        f.write(f"File: {result['file']}\n")
        f.write(f"MSE ({result['method']}): {result['mse']}\n")
        f.write("-" * 50 + "\n")
