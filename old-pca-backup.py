import os
import pydicom
import numpy as np
import sys
import matplotlib.pyplot as plt


def perform_pca(image, n_components):
    """Aplica PCA a uma imagem e retorna a imagem comprimida e os componentes principais."""
    gray_image = image.astype(np.float32)

    # Calculando a matriz de covariância
    covariance_matrix = np.cov(gray_image.T)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Ordenando os autovetores de acordo com os autovalores
    sorted_indices = np.argsort(eigenvalues)[::-1]
    principal_components = eigenvectors[:, sorted_indices][:, :n_components]

    # Comprimindo a imagem
    compressed_image = np.dot(gray_image, principal_components)

    return compressed_image, principal_components, gray_image.mean(axis=0)


def convert_dicom_to_pca_single(dicom_path, compression_percentage):
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

        # Total de componentes principais
        total_components = pixel_array.shape[1]  # Assumindo que a imagem é 2D
        n_components = int(total_components * (compression_percentage / 100))

        # Aplica PCA
        compressed_image, principal_components, mean = perform_pca(
            pixel_array, n_components
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

        reconstructed_image = np.dot(compressed_image, principal_components.T) + mean
        reconstructed_image = np.clip(reconstructed_image, 0, 255).astype(np.uint8)
        axs[1].imshow(reconstructed_image, cmap="gray")
        axs[1].set_title("Imagem Comprimida (Reconstruída)")
        axs[1].axis("off")

        plt.show()

        # Armazena os tamanhos dos arquivos
        original_size = os.path.getsize(dicom_path)  # KB
        converted_size = os.path.getsize(npz_path)  # KB

        # Exibe os resultados
        print(f"Tamanho do arquivo original: {original_size / 1024:.2f} KB")
        print(f"Tamanho do arquivo comprimido: {converted_size / 1024:.2f} KB")

    except Exception as e:
        print(f"Erro ao converter {dicom_path}: {e}")


# Exemplo de uso
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Uso: python script.py /caminho/para/arquivo_dicom porcentagem_de_compressao"
        )
        sys.exit(1)

    dicom_path = sys.argv[1]
    compression_percentage = float(sys.argv[2])  # Porcentagem a ser utilizada

    # Chama a função de conversão
    convert_dicom_to_pca_single(dicom_path, compression_percentage)
