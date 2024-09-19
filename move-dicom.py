import sys
import os
import shutil
import uuid  # To generate a random prefix


def move_dcm_files_to_root(root_dir):
    # Verifica se o diretório raiz existe
    if not os.path.isdir(root_dir):
        print(f"O diretório {root_dir} não existe.")
        return

    # Percorre todos os diretórios e arquivos a partir da raiz
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Verifica se o arquivo tem a extensão .dcm
            if file.lower().endswith(".dcm"):
                # Caminho completo do arquivo
                file_path = os.path.join(subdir, file)
                # Caminho de destino na raiz do diretório
                dest_path = os.path.join(root_dir, file)

                # Verifica se o arquivo já existe no destino para evitar sobrescrita
                if os.path.exists(dest_path):
                    # Gera um novo nome de arquivo com um prefixo aleatório
                    file_name, file_ext = os.path.splitext(file)
                    random_prefix = str(uuid.uuid4())[
                        :8
                    ]  # Usa os primeiros 8 caracteres do UUID
                    new_file_name = f"{random_prefix}_{file_name}{file_ext}"
                    dest_path = os.path.join(root_dir, new_file_name)
                    print(f"Arquivo já existe. Movendo com novo nome: {new_file_name}")

                # Move o arquivo para a raiz do diretório
                shutil.move(file_path, dest_path)
                print(f"Movido: {file_path} -> {dest_path}")


# Exemplo de uso
if __name__ == "__main__":
    # Substitua 'seu_diretorio' pelo caminho para o diretório desejado
    move_dcm_files_to_root(sys.argv[1])
