import csv
import os
import sys


# Função para atualizar ou adicionar uma linha no CSV com a taxa de compressão específica
def update_compression_csv(
    original_file_name,
    compression_method,
    compression_rate,
    original_size,
    compressed_size,
):
    csv_path = "compression_data.csv"
    # Cria um dicionário para armazenar as linhas do CSV
    rows = []
    file_exists = os.path.exists(csv_path)
    found = False

    # Converte os tamanhos para KB com duas casas decimais
    original_size_kb = f"{round(original_size / 1000, 2):.2f}"
    compressed_size_kb = f"{round(compressed_size / 1000, 2):.2f}"

    # Converte a taxa de compressão para duas casas decimais
    compression_rate = round(float(compression_rate), 2)

    # Define o nome da coluna de taxa de compressão
    compression_rate_column = f"COMPRESSAO {compression_method}"
    compressed_size_column = f"{compression_method} - TAMANHO COMPRIMIDO (KB)"

    # Se o arquivo já existir, lê as linhas para atualizar
    if file_exists:
        with open(csv_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            rows = list(reader)

            # Verifica se o arquivo original já está listado
            for row in rows:
                if row["NOME DO ARQUIVO"] == original_file_name:
                    # Atualiza apenas as colunas do método de compressão atual
                    if (
                        "TAMANHO ORIGINAL (KB)" not in row
                        or not row["TAMANHO ORIGINAL (KB)"]
                    ):
                        row["TAMANHO ORIGINAL (KB)"] = original_size_kb
                    row[compressed_size_column] = compressed_size_kb
                    row[compression_rate_column] = compression_rate
                    found = True
                    break

    # Define a ordem das colunas, garantindo que "TAMANHO ORIGINAL (KB)" esteja antes das colunas de compressão
    headers = headers if file_exists else ["NOME DO ARQUIVO", "TAMANHO ORIGINAL (KB)"]
    if compressed_size_column not in headers:
        headers.append(compressed_size_column)
    if compression_rate_column not in headers:
        headers.append(compression_rate_column)

    # Reorganiza as colunas para garantir que "TAMANHO ORIGINAL (KB)" esteja sempre antes
    headers = ["NOME DO ARQUIVO", "TAMANHO ORIGINAL (KB)"] + [
        h for h in headers if h not in ["NOME DO ARQUIVO", "TAMANHO ORIGINAL (KB)"]
    ]

    # Escreve os dados de volta no CSV
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        if not found:
            # Apenas adiciona a nova linha se ela não existir
            new_row = {
                "NOME DO ARQUIVO": original_file_name,
                "TAMANHO ORIGINAL (KB)": original_size_kb,
                compressed_size_column: compressed_size_kb,
                compression_rate_column: compression_rate,
            }
            rows.append(new_row)
            writer.writerow(new_row)


def update_mse_csv(original_file_name, compression_method, mse_value):
    csv_path = "compression_data.csv"

    # Nome da coluna de MSE
    mse_column = f"{compression_method} - MSE"

    # Lista para armazenar todas as linhas
    rows = []
    headers = []

    # Abre o CSV e lê todas as linhas
    with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        rows = list(reader)

    # Adiciona a coluna de MSE se não existir
    if mse_column not in headers:
        headers.append(mse_column)
        for row in rows:
            row[mse_column] = ""

    # Atualiza a linha correspondente
    for row in rows:
        if row["NOME DO ARQUIVO"] == original_file_name:
            row[mse_column] = f"{mse_value:.2f}"
            break

    # Escreve de volta no CSV
    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


# Torna a função utilizável em outros arquivos ao definir o módulo principal
if __name__ == "__main__":
    print()
