import numpy as np
import matplotlib.pyplot as plt
import argparse


def recreate_image_from_pca(npz_path):
    """Recria e plota a imagem a partir dos dados do arquivo NPZ contendo a imagem comprimida."""
    try:
        # Carrega os dados do arquivo NPZ
        data = np.load(npz_path)
        compressed_image = data["compressed_image"]
        principal_components = data["principal_components"]
        mean = data["mean"]

        # Reconstrói a imagem a partir dos componentes principais
        reconstructed_image = np.dot(compressed_image, principal_components) + mean
        reconstructed_image = np.clip(reconstructed_image, 0, 255).astype(np.uint8)

        # Plota a imagem reconstruída
        plt.imshow(reconstructed_image, cmap="gray")
        plt.title("Imagem Comprimida (Reconstruída)")
        plt.axis("off")
        plt.show()

    except Exception as e:
        print(f"Erro ao recriar a imagem do arquivo {npz_path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recriar e plotar uma imagem comprimida a partir de um arquivo NPZ."
    )
    parser.add_argument(
        "npz_path",
        type=str,
        help="Caminho para o arquivo NPZ que contém a imagem comprimida",
    )

    args = parser.parse_args()

    # Recria e plota a imagem a partir do arquivo NPZ
    recreate_image_from_pca(args.npz_path)
