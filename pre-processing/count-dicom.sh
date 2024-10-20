#!/bin/bash

# Verifica se o caminho do diretório foi passado como argumento
if [ -z "$1" ]; then
  echo "Por favor, forneça o caminho do diretório."
  exit 1
fi

# Conta o número de arquivos .dcm recursivamente
count=$(find "$1" -type f -iname "*.dcm" | wc -l)

# Exibe a contagem
echo "Número de arquivos .dcm na pasta '$1': $count"
