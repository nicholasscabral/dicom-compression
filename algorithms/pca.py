import numpy as np
import cv2
import os


def compress_image(image, n_components):
    # Convertendo a imagem em escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculando a matriz de covariância dos pixels da imagem
    covariance_matrix = np.cov(gray_image.T)

    # Decomposição da matriz de covariância
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Ordenando os autovetores de acordo com os autovalores correspondentes
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    # Selecionando os componentes principais
    principal_components = sorted_eigenvectors[:, :n_components]

    # Comprimindo a imagem
    compressed_image = np.dot(gray_image, principal_components)

    # Recriando a imagem a partir da compressão
    reconstructed_image = np.dot(compressed_image, principal_components.T)

    print("Número de componentes principais:", principal_components.shape[1])

    return reconstructed_image


input_file_path = "input_image.png"

# Carregando a imagem
input_image = cv2.imread(input_file_path)

# Definindo o número de componentes principais para compressão
n_components = 10

# Comprimindo a imagem
compressed_image = compress_image(input_image, n_components)

# Salvando a imagem reconstruída
cv2.imwrite("reconstructed_image.png", compressed_image)

# Calculando a diferença de tamanho entre as duas imagens
original_size_kb = os.path.getsize(input_file_path) / 1024
reconstructed_size_kb = os.path.getsize("reconstructed_image.png") / 1024
size_difference_kb = original_size_kb - reconstructed_size_kb

print(f"Tamanho da imagem original: {original_size_kb:.0f} KB")
print(f"Tamanho da imagem reconstruída: {reconstructed_size_kb:.0f} KB")
print(f"Diferença de tamanho: {size_difference_kb:.0f} KB")
print(f"Taxa de compressão: {(size_difference_kb / original_size_kb) * 100:.2f}%")


# for aux in range(10):
#     compressed_image = compress_image(input_image, (aux + 1) * 20)
#     cv2.imwrite(f"reconstructed_image_{aux}.png", compressed_image)
