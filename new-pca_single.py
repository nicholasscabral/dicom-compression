import os
import pydicom
import numpy as np
import sys
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import argparse


def perform_pca(image, variance_ratio):
    """Aplica PCA a uma imagem e retorna a imagem comprimida e os componentes principais."""
    gray_image = image.astype(np.float32)

    # Aplica PCA mantendo uma determinada porcentagem de variância
    print(variance_ratio)
    pca = PCA(variance_ratio, svd_solver="full")
    compressed_image = pca.fit_transform(gray_image)
    principal_components = pca.components_
    mean = pca.mean_

    return compressed_image, principal_components, mean


def convert_dicom_to_pca_single(dicom_path, variance_ratio):
    """Converte um arquivo DICOM em um arquivo PCA e salva em um diretório de saída."""
    # Cria o diretório de saída com sufixo '-pca-compressed'
    output_dir = os.getcwd()

    try:
        # Carrega o arquivo DICOM
        dicom = pydicom.dcmread(dicom_path, force=True)

        # Extrai os dados de pixel da imagem DICOM
        pixel_array = dicom.pixel_array

        # Normaliza os valores dos pixels para o intervalo 0-255
        pixel_array = (pixel_array - np.min(pixel_array)) / (
            np.max(pixel_array) - np.min(pixel_array)
        )
        pixel_array = (pixel_array * 255).astype(np.uint8)

        # Aplica PCA
        compressed_image, principal_components, mean = perform_pca(
            pixel_array, variance_ratio
        )

        # Define o nome do arquivo NPZ
        npz_filename = os.path.splitext(os.path.basename(dicom_path))[0] + ".npz"
        npz_path = os.path.join(output_dir, npz_filename)

        # Salva a imagem comprimida, os componentes principais e a média
        np.savez(
            npz_path,
            compressed_image=compressed_image,
            principal_components=principal_components,
            mean=mean,
        )

        # Plota a imagem original e a imagem comprimida
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        axs[0].imshow(pixel_array, cmap="gray")
        axs[0].set_title("Imagem Original")
        axs[0].axis("off")

        reconstructed_image = np.dot(compressed_image, principal_components) + mean
        reconstructed_image = np.clip(reconstructed_image, 0, 255).astype(np.uint8)
        axs[1].imshow(reconstructed_image, cmap="gray")
        axs[1].set_title("Imagem Comprimida (Reconstruída)")
        axs[1].axis("off")

        plt.show()

        # Armazena os tamanhos dos arquivos
        original_size = os.path.getsize(dicom_path)  # KB
        converted_size = os.path.getsize(npz_path)  # KB
        compression_rate = (1 - converted_size / original_size) * 100

        # Exibe os resultados
        print(f"Tamanho do arquivo original: {original_size / 1000:.2f} KB")
        print(f"Tamanho do arquivo comprimido: {converted_size / 1000:.2f} KB")
        print(f"Taxa de compressão: {compression_rate:.2f}%")

    except Exception as e:
        print(f"Erro ao converter {dicom_path}: {e}")


# Exemplo de uso
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converter um arquivo DICOM em um arquivo PCA comprimido."
    )
    parser.add_argument(
        "dicom_path",
        type=str,
        help="Caminho para o arquivo DICOM de entrada",
    )
    parser.add_argument(
        "variance_ratio",
        type=float,
        help="Quantidade de variância a ser mantida (entre 0 e 1)",
    )

    args = parser.parse_args()

    # Chama a função de conversão
    convert_dicom_to_pca_single(args.dicom_path, args.variance_ratio)
