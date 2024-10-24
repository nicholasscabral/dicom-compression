# DICOM Image Compression Analysis

## Propósito do Estudo

Este estudo investiga métodos de compressão de imagens médicas no formato DICOM, focando em algoritmos de compressão como PNG, JPEG e PCA (Principal Component Analysis). O objetivo é avaliar a relação entre a compressão de imagens e a preservação da qualidade visual, analisando métricas como MSE (Mean Squared Error) e PSNR (Peak Signal-to-Noise Ratio). O estudo tem como base imagens de tomografia dos órgãos cérebro, pulmão e mama.

## Estrutura do Projeto

### Arquivos e Diretórios

- **`main.py`**: O arquivo principal que orquestra o processo de compressão, pré-processamento e análise dos resultados.

- **`compression_data.csv` e `compression_data_backup.csv`**: Contêm os dados de compressão gerados durante o estudo, incluindo as taxas de compressão, MSE e PSNR para cada imagem comprimida.

- **Diretório `pre-processing/`**: Scripts de pré-processamento usados para preparar as imagens DICOM antes da compressão.
  - `copy-files.py`: Copia arquivos DICOM para diretórios específicos.
  - `count-dicom.sh`: Conta o número de arquivos DICOM no diretório.
  - `dicom-verify-compression.py`: Verifica a compressão de imagens no formato DICOM.

- **Diretório `algorithms/`**: Implementações dos algoritmos de compressão usados no estudo.
  - `jpeg.py`: Implementação do algoritmo de compressão JPEG.
  - `pca.py`: Implementação da compressão PCA com diferentes níveis de variância explicada.
  - `png.py`: Implementação da compressão PNG sem perda de qualidade.

- **Diretório `result-analysis/`**: Scripts para análise dos resultados da compressão.
  - `mse.py`: Calcula o MSE (Erro Médio Quadrático) das imagens comprimidas.
  - `plot-graphs.py`: Gera os gráficos usados na análise dos resultados.
  - `write_result_csv.py`: Gera arquivos CSV com os resultados da compressão.

- **Diretório `graphs/`**: Contém os gráficos gerados durante a análise dos resultados da compressão. Esses gráficos são essenciais para visualizar a relação entre o tamanho de compressão e a qualidade da imagem (MSE e PSNR) para cada tipo de órgão e algoritmo de compressão.
  - `compression_by_algorithm_and_organ.png`: Gráfico que compara a taxa de compressão para diferentes algoritmos (PNG, JPEG, PCA) em três órgãos: cérebro, pulmão e mama. Permite analisar a eficiência da compressão por algoritmo.
  - `jpeg_compression_by_organ.png`: Mostra as taxas de compressão usando o algoritmo JPEG para cada um dos órgãos estudados.
  - `pca-950_compression_by_organ.png`: Gráfico que apresenta os resultados da compressão PCA com 95% de componentes retidos.
  - `pca-975_compression_by_organ.png`: Resultados da compressão PCA com 97,5% de componentes.
  - `pca-990_compression_by_organ.png`: Resultados da compressão PCA com 99% de componentes, destacando a relação entre a quantidade de dados preservados e o nível de compressão.
  - `png_compression_by_organ.png`: Gráfico que apresenta os resultados da compressão PNG sem perda de qualidade em cada órgão.
  - `psnr_by_algorithm_and_organ.png`: Mostra a comparação do **PSNR** (Peak Signal-to-Noise Ratio) para cada algoritmo de compressão e órgão, destacando a qualidade da imagem após a compressão.

- **Diretório `misc/`**: Scripts auxiliares usados no estudo.
  - `decompress-npz.py`: Script para descompactar e reconstruir arquivos NPZ.
  - `pca-components-percentage.py`: Análise da porcentagem de variância explicada pelos componentes principais na compressão PCA.
  - `reconstructed_image.png`: Imagem reconstruída de uma compressão PCA para visualização da qualidade.

## Conclusão

Este projeto oferece uma análise detalhada sobre como diferentes algoritmos de compressão afetam a qualidade de imagens médicas DICOM. Ele visa auxiliar na escolha de técnicas de compressão eficientes para armazenamento de dados médicos, equilibrando entre o tamanho do arquivo e a preservação da qualidade.
