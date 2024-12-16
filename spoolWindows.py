import os
import subprocess
import time
import shutil

def restart_spooler():
    """Reinicia o serviço de spooler de impressão"""
    subprocess.call(["net", "stop", "spooler"])
    time.sleep(2)
    subprocess.call(["net", "start", "spooler"])

def is_spooler_running():
    """Verifica se o serviço de spooler está em execução."""
    result = subprocess.run(["sc", "query", "spooler"], capture_output=True, text=True)
    return "RUNNING" in result.stdout

def backup_print_queue(printers_folder, backup_folder):
    """Faz backup dos arquivos de impressão antes de deletá-los."""
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    for root, dirs, files in os.walk(printers_folder):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                shutil.copy(file_path, backup_folder)
                print(f"Arquivo {file_path} copiado para backup.")
            except Exception as e:
                print(f"Não foi possível copiar o arquivo {file_path} para backup: {e}")

def clear_print_queue(printers_folder, log_file):
    """Remove todos os arquivos na pasta de spool de impressão e registra as ações."""
    with open(log_file, 'a') as log:
        for root, dirs, files in os.walk(printers_folder):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    log.write(f"{time.ctime()}: Arquivo {file_path} removido com sucesso.\n")
                except Exception as e:
                    log.write(f"{time.ctime()}: Não foi possível remover o arquivo {file_path}: {e}\n")

def main():
    printers_folder = r'C:\Windows\System32\spool\PRINTERS'
    backup_folder = r'C:\Backup\Spooler'
    log_file = r'C:\Logs\spooler_cleanup.log'

    print("Verificando serviço de spooler de impressão...")

    # Reiniciar o serviço de spooler de impressão
    restart_spooler()

    # Verificar se o spooler está rodando
    if is_spooler_running():
        print("Serviço de spooler em execução.")
    else:
        print("Erro: Serviço de spooler não está em execução.")
        return

    # Fazer backup dos arquivos de impressão
    print("Fazendo backup dos arquivos de impressão...")
    backup_print_queue(printers_folder, backup_folder)

    # Limpar a fila de impressão presa
    print("Limpando a fila de impressão...")
    clear_print_queue(printers_folder, log_file)

    print("Fila de impressão desobstruída com sucesso.")

if __name__ == "__main__":
    main()
