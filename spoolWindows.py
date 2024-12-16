import os
import sys
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

def check_permissions():
    """Verifica se o script está sendo executado com permissões de administrador."""
    if not os.name == 'nt' or not os.system("fltmc") == 0:
        print("Erro: Este script precisa ser executado com permissões de administrador.")
        sys.exit(1)

def parse_arguments():
    """Analisa os argumentos de linha de comando."""
    import argparse
    parser = argparse.ArgumentParser(description="Limpa a fila de impressão e faz backup dos arquivos.")
    parser.add_argument('--printers-folder', type=str, default=r'C:\Windows\System32\spool\PRINTERS',
                        help="Pasta de spool de impressão")
    parser.add_argument('--backup-folder', type=str, default=r'C:\Backup\Spooler',
                        help="Pasta para backup dos arquivos de impressão")
    parser.add_argument('--log-file', type=str, default=r'C:\Logs\spooler_cleanup.log',
                        help="Arquivo de log")
    return parser.parse_args()

def main():
    args = parse_arguments()

    printers_folder = args.printers_folder
    backup_folder = args.backup_folder
    log_file = args.log_file

    check_permissions()

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
    print(f"Backup salvo em: {backup_folder}")
    print(f"Log de ações salvo em: {log_file}")

if __name__ == "__main__":
    main()
