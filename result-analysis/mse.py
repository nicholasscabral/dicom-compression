import os
import numpy as np
import pydicom
from PIL import Image
from write_result_csv import update_mse_psnr_csv  # Import the CSV update function


def calculate_mse(original_image, compressed_image):
    """Calcula o MSE entre duas imagens"""
    mse = np.mean((original_image - compressed_image) ** 2)
    return round(mse, 2)  # Round to two decimal places


def calculate_psnr(mse, max_pixel=255.0):
    """Calcula o PSNR baseado no MSE"""
    if mse == 0:
        return float("inf")  # Retorna infinito se não há diferença
    psnr = 10 * np.log10((max_pixel**2) / mse)
    return round(psnr, 2)  # Round to two decimal places


def normalize_image(image):
    """Normaliza a imagem para a faixa de 0 a 255"""
    return ((image - np.min(image)) / (np.max(image) - np.min(image)) * 255).astype(
        np.uint8
    )


def read_dicom_image(path):
    """Lê uma imagem DICOM e a normaliza"""
    ds = pydicom.dcmread(path)
    return normalize_image(ds.pixel_array.astype(np.float32))


def read_image(path, is_pca=False):
    """Lê uma imagem comprimida por PCA ou um arquivo PNG/JPEG"""
    if is_pca:
        data = np.load(path)
        compressed_image = data["compressed_image"]
        principal_components = data["principal_components"]
        mean = data["mean"]

        # Reconstroi a imagem usando os componentes principais
        reconstructed_image = np.dot(compressed_image, principal_components) + mean

        # Clampeia os valores da imagem reconstruída para garantir que estejam dentro da faixa [0, 255]
        reconstructed_image = np.clip(reconstructed_image, 0, 255).astype(np.uint8)

        return reconstructed_image
    else:
        return np.array(Image.open(path).convert("L"), dtype=np.uint8)


def process_images(original_directory, compressed_directories, compressed_extensions):
    """Processa as imagens originais e comprimidas, calculando o MSE e PSNR para cada método"""
    results = []

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

            # Calcula o MSE
            mse = calculate_mse(original_image, compressed_image)

            # Calcula o PSNR com base no MSE
            psnr = calculate_psnr(mse)

            # Build the method name
            pca_method_mapping = {
                "pca95": "PCA-950",
                "pca975": "PCA-975",
                "pca99": "PCA-990",
            }

            if method.startswith("pca"):
                method_name = pca_method_mapping.get(method, f"PCA-{method[3:]}")
            else:
                method_name = method.upper()

            # Collect the result
            results.append(
                {
                    "original_file_name": f"{os.path.basename(original_directory)}/{file}",
                    "compression_method": method_name,
                    "mse_value": mse,
                    "psnr_value": psnr,  # Adiciona o PSNR junto com o MSE
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

# Atualiza o CSV com os resultados (incluindo MSE e PSNR)
update_mse_psnr_csv(all_results)
