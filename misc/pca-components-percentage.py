import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt


def load_dicom_image(dicom_path):
    """Carrega e normaliza uma imagem DICOM para escala de cinza 0-255."""
    dicom_image = pydicom.dcmread(dicom_path)
    pixel_array = dicom_image.pixel_array

    # Normalizando a imagem para 0-255
    pixel_array = (pixel_array - np.min(pixel_array)) / (
        np.max(pixel_array) - np.min(pixel_array)
    )
    pixel_array = (pixel_array * 255).astype(np.uint8)

    return pixel_array


def perform_pca(image, component_percentage):
    """Aplica PCA a uma imagem e retorna a imagem comprimida e os componentes principais."""
    gray_image = image.astype(np.float32)

    # Calculando a matriz de covariância e autovetores
    covariance_matrix = np.cov(gray_image.T)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Ordenando os autovalores e autovetores (em ordem decrescente)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # Selecionando o número de componentes baseado no percentual de componentes desejado
    n_components = int(len(eigenvalues) * (component_percentage / 100))

    # Selecionando os principais componentes
    principal_components = eigenvectors[:, :n_components]

    # Comprimindo a imagem usando os principais componentes
    compressed_image = np.dot(gray_image, principal_components)

    return compressed_image.astype(np.float16), principal_components.astype(np.float16)


def save_compressed_image(compressed_image, principal_components, save_path):
    """Salva a imagem comprimida e os componentes principais em um arquivo .npz."""
    np.savez_compressed(
        save_path,
        compressed_image=compressed_image,
        principal_components=principal_components,
    )
    print(f"Imagem comprimida salva em: {save_path}")


def reconstruct_image(compressed_image, principal_components):
    """Reconstrói a imagem comprimida usando os componentes principais."""
    return np.dot(compressed_image, principal_components.T)


def plot_images(original_image, reconstructed_image):
    """Exibe a imagem original e a reconstruída lado a lado."""
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.title("Imagem Original")
    if original_image is not None:
        plt.imshow(original_image, cmap="gray")
    else:
        plt.text(0.5, 0.5, "Imagem Original Não Disponível", ha="center", va="center")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Imagem Reconstruída (PCA)")
    plt.imshow(reconstructed_image, cmap="gray")
    plt.axis("off")

    plt.show()


def process_dicom_image(dicom_path, component_percentage, compressed_path):
    """Processa uma imagem DICOM, aplica PCA e salva a imagem comprimida."""
    original_image = load_dicom_image(dicom_path)
    compressed_image, principal_components = perform_pca(
        original_image, component_percentage
    )
    save_compressed_image(compressed_image, principal_components, compressed_path)

    # Exibir tamanhos e taxa de compressão
    original_size_kb = os.path.getsize(dicom_path) / 1024
    compressed_size_kb = os.path.getsize(compressed_path) / 1024
    compression_ratio = (1 - compressed_size_kb / original_size_kb) * 100

    print(f"Tamanho da imagem original: {original_size_kb:.2f} KB")
    print(f"Tamanho do arquivo .npz (imagem comprimida): {compressed_size_kb:.2f} KB")
    print(f"Taxa de Compressão: {compression_ratio:.2f}%")

    # Reconstruindo a imagem
    reconstructed_image = reconstruct_image(compressed_image, principal_components)

    # Plotando as imagens original e reconstruída
    plot_images(original_image, reconstructed_image)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print(
            "Uso: python script.py /caminho/para/imagem.dcm percentual_componentes /caminho/para/arquivo_comprimido.npz"
        )
        sys.exit(1)

    dicom_path = sys.argv[1]
    component_percentage = float(sys.argv[3])  # Percentual de componentes principais
    compressed_path = sys.argv[2]

    process_dicom_image(dicom_path, component_percentage, compressed_path)
