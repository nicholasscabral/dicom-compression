import os
import shutil
import pydicom


def copy_dicom_by_resolution(input_dir, resolution, max_images):
    # Gera o caminho da pasta de saída (input_dir -copy)
    output_dir = input_dir.rstrip(os.sep) + f"-{resolution}"

    # Verifica se o diretório de entrada existe
    if not os.path.isdir(input_dir):
        print(f"O diretório {input_dir} não existe.")
        return

    # Cria a pasta de saída se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Conta o número de arquivos copiados
    copied_files = 0

    # Percorre todos os diretórios e arquivos a partir da pasta de entrada
    for subdir, _, files in os.walk(input_dir):
        for file in files:
            # Verifica se o arquivo tem a extensão .dcm
            if file.lower().endswith(".dcm"):
                file_path = os.path.join(subdir, file)

                try:
                    # Carrega a imagem DICOM
                    dicom_image = pydicom.dcmread(file_path)

                    # Verifica se a imagem possui dados de pixels e se é grayscale 2D
                    if (
                        not hasattr(dicom_image, "pixel_array")
                        or len(dicom_image.pixel_array.shape) != 2
                    ):
                        continue

                    # Verifica se o tipo de dados do pixel array é suportado
                    if dicom_image.pixel_array.dtype not in [
                        "uint8",
                        "uint16",
                        "int16",
                        "int8",
                    ]:
                        print(
                            f"Arquivo {file_path} ignorado devido ao tipo de dado não suportado: {dicom_image.pixel_array.dtype}"
                        )
                        continue

                    # Obtém a resolução da imagem DICOM
                    pixel_array = dicom_image.pixel_array
                    rows, columns = pixel_array.shape
                    dicom_resolution = f"{columns}x{rows}"

                    # Verifica se a resolução corresponde à desejada
                    if dicom_resolution == resolution:
                        # Copia o arquivo para a pasta de saída
                        shutil.copy(file_path, output_dir)
                        print(f"Copiado: {file_path} -> {output_dir}")
                        copied_files += 1

                        # Verifica se atingiu o número máximo de imagens
                        if copied_files >= max_images:
                            print(f"\nNúmero máximo de {max_images} imagens atingido.")
                            return
                except Exception as e:
                    print(f"Erro ao processar {file_path}: {e}")

    print(f"\nTotal de arquivos copiados: {copied_files}")


# Exemplo de uso
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print(
            "Uso: python script.py /caminho/para/pasta_de_entrada resolucao_ex:512x512 quantidade_maxima"
        )
        sys.exit(1)

    input_dir = sys.argv[1]
    resolution = sys.argv[2]
    max_images = int(sys.argv[3])

    copy_dicom_by_resolution(input_dir, resolution, max_images)
