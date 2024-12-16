import os
import subprocess
import time

def restart_spooler():
    subprocess.call(["net", "stop", "spooler"])
    time.sleep(2)
    subprocess.call(["net", "start", "spooler"])

def clear_print_queue(printers_folder):
    for root, dirs, files in os.walk(printers_folder):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Arquivo {file_path} removido com sucesso.")
            except Exception as e:
                print(f"Não foi possível remover o arquivo {file_path}: {e}")

def main():
    printers_folder = r'C:\Windows\System32\spool\PRINTERS'
    print("Verificando serviço de spooler de impressão...")

    # Reiniciar o serviço de spooler de impressão
    restart_spooler()

    # Limpar a fila de impressão presa
    print("Limpando a fila de impressão...")
    clear_print_queue(printers_folder)

    print("Fila de impressão desobstruída com sucesso.")

if __name__ == "__main__":
    main()
