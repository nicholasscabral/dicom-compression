import subprocess
import sys


def run_commands_sequentially(commands):
    for command in commands:
        try:
            # Verifica se o último parâmetro do comando é um número e o converte para string se necessário
            if isinstance(command[-1], (int, float)):
                command = command[:-1] + [str(command[-1])]

            # Imprime o comando que será executado
            print(f"Executando: {' '.join(command)}")

            # Executa o comando
            result = subprocess.run(command, check=True)

            # Verifica se a execução foi bem-sucedida
            if result.returncode == 0:
                print(f"Comando {' '.join(command)} executado com sucesso!\n")
            else:
                print(f"Comando {' '.join(command)} terminou com erros.\n")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o comando {' '.join(command)}: {e}")
        except FileNotFoundError:
            print(f"Comando não encontrado: {' '.join(command)}")
        except Exception as e:
            print(f"Erro desconhecido ao executar o comando {' '.join(command)}: {e}")


# Exemplo de uso
if __name__ == "__main__":
    # Definir comandos a serem executados
    path_lung = "/media/nicholas/files/tcc-cancer-images/lung-512x512"
    path_breast = "/media/nicholas/files/tcc-cancer-images/breast-512x512"
    path_brain = "/media/nicholas/files/tcc-cancer-images/brain-512x512"

    commands = [
        # PNG compression
        ["python3", "algorithms/png.py", path_lung],
        ["python3", "algorithms/png.py", path_breast],
        ["python3", "algorithms/png.py", path_brain],
        # JPEG compression
        ["python3", "algorithms/jpeg.py", path_lung],
        ["python3", "algorithms/jpeg.py", path_breast],
        ["python3", "algorithms/jpeg.py", path_brain],
        # PCA compression - LUNG
        ["python3", "algorithms/new-pca.py", path_lung, 0.95],
        ["python3", "algorithms/new-pca.py", path_lung, 0.975],
        ["python3", "algorithms/new-pca.py", path_lung, 0.99],
        # PCA compression - BREAST
        ["python3", "algorithms/new-pca.py", path_breast, 0.95],
        ["python3", "algorithms/new-pca.py", path_breast, 0.975],
        ["python3", "algorithms/new-pca.py", path_breast, 0.99],
        # PCA compression - BRAIN
        ["python3", "algorithms/new-pca.py", path_brain, 0.95],
        ["python3", "algorithms/new-pca.py", path_brain, 0.975],
        ["python3", "algorithms/new-pca.py", path_brain, 0.99],
    ]

    run_commands_sequentially(commands)
