import os
import numpy as np
import pydicom
from sklearn.decomposition import PCA
import argparse
from PIL import Image


# Função para carregar uma imagem DICOM e convertê-la em um array numpy
def load_dicom_image(file_path):
    dicom = pydicom.dcmread(file_path)
    image = dicom.pixel_array
    return image


# Função para aplicar PCA para compressão da imagem
def apply_pca_compression(image, variance_ratio):
    # Normaliza a imagem para ter valores entre 0 e 1
    image_normalized = image / 255.0

    # Aplica PCA mantendo a quantidade de variância especificada
    pca = PCA(n_components=variance_ratio, svd_solver="full")
    compressed_image = pca.fit_transform(image_normalized)

    # Retorna a imagem comprimida e o objeto PCA para reconstrução posterior
    return compressed_image, pca


# Função para converter e comprimir um diretório de imagens DICOM usando PCA
def convert_dicom_to_pca(input_dir, variance_ratio):
    """
    Converte arquivos DICOM em arquivos PCA comprimidos e salva em um diretório de saída.
    """
    # Cria o diretório de saída com sufixo '-pca-compressed' e a variância informada
    output_dir = f"{input_dir}-pca-compressed-{int(variance_ratio * 1000)}"
    os.makedirs(output_dir, exist_ok=True)

    # Listas para armazenar tamanhos dos arquivos
    original_sizes = []
    converted_sizes = []

    # Percorre todos os arquivos no diretório de entrada
    for subdir, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".dcm"):
                dicom_path = os.path.join(subdir, file)

                try:
                    # Carrega o arquivo DICOM
                    image = load_dicom_image(dicom_path)

                    # Verifica se a imagem é grayscale
                    if len(image.shape) != 2:
                        raise ValueError("A imagem DICOM não é grayscale.")

                    # Aplica PCA com a variância informada
                    compressed_image, pca = apply_pca_compression(image, variance_ratio)

                    # Define o nome do arquivo NPZ e TIFF
                    npz_filename = os.path.splitext(file)[0] + ".npz"
                    npz_path = os.path.join(output_dir, npz_filename)

                    # Salva a imagem comprimida e os componentes principais em NPZ
                    np.savez_compressed(
                        npz_path,
                        compressed_image=compressed_image,
                        components=pca.components_,
                        mean=pca.mean_,
                    )

                    # Armazena os tamanhos dos arquivos
                    original_size = os.path.getsize(dicom_path)  # bytes
                    converted_size = os.path.getsize(npz_path)  # bytes

                    # print(
                    #     f"Tamanho original: {original_size} bytes, Comprimido: {converted_size} bytes"
                    # )

                    print(
                        f"{subdir.split('/')[-1]}/{file} => {(1 - converted_size / original_size) * 100:.2f}%"
                    )

                    original_sizes.append(original_size)
                    converted_sizes.append(converted_size)

                except Exception as e:
                    print(f"Erro ao converter {dicom_path}: {e}")

    # Calcula estatísticas
    mean_original_size = np.mean(original_sizes)
    mean_converted_size = np.mean(converted_sizes)
    compression_ratios = [o / c for o, c in zip(original_sizes, converted_sizes)]
    mean_compression_ratio = 1 - np.mean(compression_ratios)
    std_dev_compression_ratio = np.std(compression_ratios)

    # Exibe os resultados
    print(f"\nTotal de arquivos convertidos: {len(original_sizes)}")
    print(f"Tamanho médio do arquivo original: {mean_original_size / 1024:.2f} KB")
    print(f"Tamanho médio do arquivo comprimido: {mean_converted_size / 1024:.2f} KB")
    print(f"Taxa de compressão média: {mean_compression_ratio * 100:.2f}%")
    print(f"Desvio padrão da taxa de compressão: {std_dev_compression_ratio:.2f}")


# Exemplo de uso
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converter um diretório de imagens DICOM em arquivos PCA comprimidos."
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="Caminho para o diretório de imagens DICOM de entrada",
    )
    parser.add_argument(
        "variance_ratio",
        type=float,
        help="Quantidade de variância a ser mantida (entre 0 e 1)",
    )

    args = parser.parse_args()
    # Chama a função de conversão
    convert_dicom_to_pca(args.input_dir, args.variance_ratio)
