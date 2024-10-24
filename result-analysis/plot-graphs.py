# Importar as bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Criar diretório para salvar os gráficos
os.makedirs("./graphs", exist_ok=True)


# Função para carregar e preparar os dados
def load_and_prepare_data(file_path):
    new_data = pd.read_csv(file_path)
    new_data["TIPO DE IMAGEM"] = new_data["NOME DO ARQUIVO"].apply(
        lambda x: "Cérebro" if "brain" in x else "Mama" if "breast" in x else "Pulmão"
    )
    new_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    average_metrics = (
        new_data.groupby("TIPO DE IMAGEM")
        .agg(
            {
                "COMPRESSAO PNG": "mean",
                "COMPRESSAO JPEG": "mean",
                "COMPRESSAO PCA-950": "mean",
                "COMPRESSAO PCA-975": "mean",
                "COMPRESSAO PCA-990": "mean",
                "MSE PNG": "mean",
                "PSNR PNG": "mean",
                "MSE JPEG": "mean",
                "PSNR JPEG": "mean",
                "MSE PCA-950": "mean",
                "PSNR PCA-950": "mean",
                "MSE PCA-975": "mean",
                "PSNR PCA-975": "mean",
                "MSE PCA-990": "mean",
                "PSNR PCA-990": "mean",
            }
        )
        .reset_index()
    )
    return average_metrics


# Função para gerar gráfico de comparação de PCA
def plot_pca_comparison(average_metrics, output_dir):
    for pca_method in [
        "COMPRESSAO PCA-950",
        "COMPRESSAO PCA-975",
        "COMPRESSAO PCA-990",
    ]:
        plt.figure(figsize=(10, 6))
        plt.bar(
            average_metrics["TIPO DE IMAGEM"],
            average_metrics[pca_method],
            color="lightblue",
        )
        plt.title(f"Taxas Médias de Compressão por Tipo de Órgão para {pca_method}")
        plt.xlabel("Tipo de Órgão")
        plt.ylabel("Taxa de Compressão (%)")
        plt.ylim(0, 100)
        for idx, value in enumerate(average_metrics[pca_method]):
            plt.text(idx, value + 1, f"{value:.2f}%", ha="center")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(
            f"{output_dir}/{pca_method.split(' ')[1].lower()}_compression_by_organ.png"
        )
        plt.close()


# Função para gerar gráfico de comparação do JPEG
def plot_jpeg_comparison(average_metrics, output_dir):
    plt.figure(figsize=(10, 6))
    plt.bar(
        average_metrics["TIPO DE IMAGEM"],
        average_metrics["COMPRESSAO JPEG"],
        color="lightgreen",
    )
    plt.title("Taxas Médias de Compressão JPEG por Tipo de Órgão")
    plt.xlabel("Tipo de Órgão")
    plt.ylabel("Taxa de Compressão (%)")
    plt.ylim(0, 100)
    for idx, value in enumerate(average_metrics["COMPRESSAO JPEG"]):
        plt.text(idx, value + 1, f"{value:.2f}%", ha="center")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/jpeg_compression_by_organ.png")
    plt.close()


# Função para gerar gráfico de comparação do PNG
def plot_png_comparison(average_metrics, output_dir):
    plt.figure(figsize=(10, 6))
    plt.bar(
        average_metrics["TIPO DE IMAGEM"],
        average_metrics["COMPRESSAO PNG"],
        color="orange",
    )
    plt.title("Taxas Médias de Compressão PNG por Tipo de Órgão")
    plt.xlabel("Tipo de Órgão")
    plt.ylabel("Taxa de Compressão (%)")
    plt.ylim(0, 100)
    for idx, value in enumerate(average_metrics["COMPRESSAO PNG"]):
        plt.text(idx, value + 1, f"{value:.2f}%", ha="center")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/png_compression_by_organ.png")
    plt.close()


# Função para gerar gráfico comparando todos os métodos de compressão
def plot_compression_comparison(
    average_metrics,
    compression_methods,
    compression_methods_adjusted,
    colors,
    output_dir,
):
    x = np.arange(
        len(average_metrics["TIPO DE IMAGEM"])
    )  # posições dos rótulos dos tipos de órgãos
    width = 0.15  # largura das barras

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plotar cada método de compressão como barras agrupadas
    for i, (method, color) in enumerate(zip(compression_methods, colors)):
        ax.bar(
            x + i * width,
            average_metrics[method],
            width,
            label=compression_methods_adjusted[i],
            color=color,
        )
        for idx, value in enumerate(average_metrics[method]):
            ax.text(idx + i * width, value + 1, f"{value:.2f}%", ha="center")

    # Adicionar rótulos, título e personalizar rótulos do eixo x
    ax.set_xlabel("Tipo de Órgão")
    ax.set_ylabel("Taxa de Compressão (%)")
    ax.set_title("Taxas Médias de Compressão por Tipo de Órgão e Método")
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(average_metrics["TIPO DE IMAGEM"])
    ax.legend(title="Método de Compressão")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/compression_by_algorithm_and_organ.png")
    plt.close()


# Função para gerar gráfico de PSNR por algoritmo e tipo de órgão
def plot_psnr_comparison(
    average_metrics, compression_methods_adjusted, colors, output_dir
):
    x = np.arange(
        len(compression_methods_adjusted)
    )  # posições dos rótulos para os métodos de compressão
    width = 0.25  # largura das barras

    fig, ax = plt.subplots(figsize=(14, 8))

    # Plotar PSNR para cada tipo de órgão como barras agrupadas
    infinite_written = False  # Variável para controlar se "Infinito" já foi escrito
    for i, (image_type, color) in enumerate(
        zip(average_metrics["TIPO DE IMAGEM"], colors)
    ):
        values = average_metrics.iloc[i][
            ["PSNR PNG", "PSNR JPEG", "PSNR PCA-950", "PSNR PCA-975", "PSNR PCA-990"]
        ].values  # Selecionar valores de PSNR da linha i
        ax.bar(x + i * width, values, width, label=image_type, color=color)
        for idx, value in enumerate(values):
            if (
                np.isnan(value) and not infinite_written
            ):  # Verificar se o valor é NaN devido ao infinito e se já não foi escrito
                ax.text(
                    idx + i * width,
                    1,
                    "Infinito",
                    ha="center",
                    color="red",
                    fontsize=10,
                    fontweight="bold",
                )
                infinite_written = True  # Marcar que "Infinito" já foi escrito
            elif not np.isnan(value):
                ax.text(idx + i * width, value + 0.5, f"{value:.2f}", ha="center")

    # Adicionar rótulos, título e personalizar rótulos do eixo x
    ax.set_xlabel("Algoritmos de Compressão")
    ax.set_ylabel("Pico de Relação Sinal-Ruído (PSNR) [dB]")
    ax.set_title(
        "Valores Médios de PSNR por Algoritmo e Tipo de Órgão (Com Zonas de Qualidade)"
    )
    ax.set_xticks(x + width)
    ax.set_xticklabels(compression_methods_adjusted)
    ax.legend(title="Tipo de Órgão")

    # Adicionar faixas de qualidade no eixo y e limitar a escala
    plt.axhspan(40, 50, color="lightgreen", alpha=0.2, label="Zona Alta Qualidade")
    plt.axhspan(30, 40, color="yellow", alpha=0.2, label="Zona Boa Qualidade")
    plt.axhspan(20, 30, color="orange", alpha=0.2, label="Zona Qualidade Regular")
    plt.axhspan(0, 20, color="red", alpha=0.2, label="Zona Baixa Qualidade")

    plt.ylim(0, 50)  # Limitar o eixo Y até 50
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(title="Zonas de Qualidade", loc="upper left")
    plt.savefig(f"{output_dir}/psnr_by_algorithm_and_organ.png")
    plt.close()


# Caminho do arquivo CSV
new_file_path = "compression_data.csv"

# Carregar e preparar os dados
average_metrics = load_and_prepare_data(new_file_path)

# Definindo métodos de compressão e cores
compression_methods = [
    "COMPRESSAO PNG",
    "COMPRESSAO JPEG",
    "COMPRESSAO PCA-950",
    "COMPRESSAO PCA-975",
    "COMPRESSAO PCA-990",
]
compression_methods_adjusted = ["PNG", "JPEG", "PCA-95", "PCA-97,5", "PCA-99"]
colors = ["skyblue", "lightgreen", "pink", "orange", "lightgray"]
output_dir = "./graphs"

# Gerar os gráficos no diretório especificado
plot_pca_comparison(average_metrics, output_dir)
plot_jpeg_comparison(average_metrics, output_dir)
plot_png_comparison(average_metrics, output_dir)
plot_psnr_comparison(average_metrics, compression_methods_adjusted, colors, output_dir)
plot_compression_comparison(
    average_metrics,
    compression_methods,
    compression_methods_adjusted,
    colors,
    output_dir,
)
