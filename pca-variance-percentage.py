import numpy as np
import pydicom
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import argparse


# Função para carregar uma imagem DICOM e convertê-la em um array numpy
def load_dicom_image(file_path):
    dicom = pydicom.dcmread(file_path)
    image = dicom.pixel_array
    return image


# Função para aplicar PCA para compressão da imagem
def apply_pca_compression(image, variance_ratio):
    # Normaliza a imagem para ter valores entre 0 e 1
    image_normalized = image / 255.0

    # Aplica PCA nas linhas da imagem
    pca = PCA(n_components=variance_ratio, svd_solver="full")
    compressed_image = pca.fit_transform(image_normalized)

    # Retorna a imagem comprimida e o objeto PCA para reconstrução posterior
    return compressed_image, pca


# Função principal para comprimir uma imagem DICOM e salvar como .npz
def compress_dicom_image(input_path, output_path, variance_ratio):
    # Carrega a imagem DICOM
    image = load_dicom_image(input_path)

    # Verifica se a imagem é grayscale
    if len(image.shape) != 2:
        raise ValueError("A imagem DICOM não é grayscale.")

    # Aplica a compressão PCA
    compressed_image, pca = apply_pca_compression(image, variance_ratio)

    # Salva a imagem comprimida e os componentes principais em um arquivo .npz
    np.savez_compressed(
        output_path,
        compressed_image=compressed_image,
        components=pca.components_,
        mean=pca.mean_,
    )
    print(f"Imagem comprimida salva em: {output_path}")

    # Calcula e imprime a taxa de compressão
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    compression_ratio = (1 - compressed_size / original_size) * 100
    print(f"Tamanho original: {original_size / 1024:.2f} KB")
    print(f"Tamanho comprimido: {compressed_size / 1024:.2f} KB")
    print(f"Taxa de compressão: {compression_ratio:.2f}%")

    # Exibe a imagem original e a imagem comprimida
    reconstructed_image = pca.inverse_transform(compressed_image) * 255.0

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].imshow(image, cmap="gray")
    axs[0].set_title("Imagem Original")
    axs[0].axis("off")

    axs[1].imshow(reconstructed_image, cmap="gray")
    axs[1].set_title(
        f"Imagem Comprimida (Reconstruída) - {variance_ratio*100:.1f}% Variância"
    )
    axs[1].axis("off")

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Comprimir uma imagem DICOM usando PCA e salvar como .npz"
    )
    parser.add_argument(
        "input_path", type=str, help="Caminho para a imagem DICOM de entrada"
    )
    parser.add_argument(
        "output_path", type=str, help="Caminho para salvar a imagem comprimida"
    )
    parser.add_argument(
        "variance_ratio",
        type=float,
        help="Quantidade de variância a ser mantida (entre 0 e 1)",
    )

    args = parser.parse_args()

    # Comprime a imagem DICOM e salva
    compress_dicom_image(args.input_path, args.output_path, args.variance_ratio)
