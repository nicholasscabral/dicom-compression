import os
import pydicom
from PIL import Image
import numpy as np


def convert_dicom_to_jpeg(input_dir):
    # Cria o diretório de saída com sufixo '-jpeg-compressed'
    output_dir = input_dir + "-jpeg-compressed"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Listas para armazenar tamanhos dos arquivos
    original_sizes = []
    converted_sizes = []
    compression_rates = []

    # Percorre todos os arquivos no diretório de entrada
    for subdir, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".dcm"):
                dicom_path = os.path.join(subdir, file)

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

                    # Converte a matriz de pixels em uma imagem Pillow
                    image = Image.fromarray(pixel_array)

                    # Define o nome do arquivo JPEG
                    jpeg_filename = os.path.splitext(file)[0] + ".jpeg"
                    jpeg_path = os.path.join(output_dir, jpeg_filename)

                    # Salva a imagem como JPEG
                    image.save(jpeg_path, format="JPEG")

                    # Armazena os tamanhos dos arquivos
                    original_size = os.path.getsize(dicom_path) * 1000  # KB
                    converted_size = os.path.getsize(jpeg_path) * 1000  # KB
                    compression_rate = (1 - converted_size / original_size) * 100

                    original_sizes.append(original_size)
                    converted_sizes.append(converted_size)
                    compression_rates.append(compression_rate)

                except Exception as e:
                    print(f"Erro ao converter {dicom_path}: {e}")

    # Calcula estatísticas
    mean_original_size = np.mean(original_sizes)
    mean_converted_size = np.mean(converted_sizes)
    mean_compression_rate = np.mean(compression_rates)
    std_dev_compression_rate = np.std(compression_rates)

    # Exibe os resultados
    print(f"\nTotal de arquivos convertidos: {len(original_sizes)}")
    print(f"Tamanho médio do arquivo original: {mean_original_size / (1024**2):.2f} Kb")
    print(
        f"Tamanho médio do arquivo convertido: {mean_converted_size / (1024**2):.2f} Kb"
    )
    print(f"Taxa de compressão média: {mean_compression_rate:.2f}%")
    print(f"Desvio padrão da taxa de compressão: {std_dev_compression_rate:.2f}")


# Exemplo de uso
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python script.py /caminho/para/pasta_de_entrada")
        sys.exit(1)

    input_dir = sys.argv[1]

    # Chama a função de conversão
    convert_dicom_to_jpeg(input_dir)
