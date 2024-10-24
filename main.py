import subprocess
import sys


def run_commands_sequentially(commands):
    for command in commands:
        try:
            if isinstance(command[-1], (int, float)):
                command = command[:-1] + [str(command[-1])]

            print(f"Executando: {' '.join(command)}")

            result = subprocess.run(command, check=True)

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
        ["python3", "algorithms/pca.py", path_lung, 0.95],
        ["python3", "algorithms/pca.py", path_lung, 0.975],
        ["python3", "algorithms/pca.py", path_lung, 0.99],
        # PCA compression - BREAST
        ["python3", "algorithms/pca.py", path_breast, 0.95],
        ["python3", "algorithms/pca.py", path_breast, 0.975],
        ["python3", "algorithms/pca.py", path_breast, 0.99],
        # PCA compression - BRAIN
        ["python3", "algorithms/pca.py", path_brain, 0.95],
        ["python3", "algorithms/pca.py", path_brain, 0.975],
        ["python3", "algorithms/pca.py", path_brain, 0.99],
        # Calculate MSE and PSNR
        ["python3", "result-analysis/mse-psnr.py"],
        # Plot graphs
        ["python3", "result-analysis/plot-graphs.py"],
    ]

    run_commands_sequentially(commands)
