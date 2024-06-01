import subprocess
import sys
import os

#variavel das cores
cor_vermelha = "\033[1;31m"
cor_verde = "\033[1;32m"
cor_amarela = "\033[1;33m"
cor_azul = "\033[1;34m"
cor_roxa = "\033[1;35m"
cor_ciano = "\033[1;36m"
cor_branca = "\033[1;37m"
cor_reset = "\033[0m"  

def instalar_bibliotecas_necessarias():
    bibliotecas = [
    "win10toast",
    "requests",
    "customtkinter",
    "datetime"
    ]

    print(f"\n{cor_amarela}[!] Verificando bibliotecas...{cor_reset}")

    for biblioteca in bibliotecas:
        print(f"{cor_reset}[{cor_amarela}*{cor_reset}]{cor_amarela} Verificando {biblioteca}{cor_reset}")
        try:
            __import__(biblioteca)
            print(f"{cor_reset}[{cor_azul}+{cor_reset}]{cor_verde} {biblioteca} Verificada {cor_reset}")
        except ImportError:
            print(f"{cor_reset}[{cor_vermelha}-{cor_reset}]{cor_vermelha} Instalando biblioteca {biblioteca}{cor_reset}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", biblioteca])

def verificar_e_definir_flag():
    flag_path = "conf/flag.txt"

    if os.path.exists(flag_path):
        with open(flag_path, "r") as file:
            flag_status = file.read().strip()
    else:
        flag_status = "False"

    return flag_status

def setar_flag_true():
    flag_path = "conf/flag.txt"

    with open(flag_path, "w") as file:
        file.write("True")



def imprimir_banner():
    banner = """
.____  ____   ____              .__   _____         
|    | \   \ /   / ____ _______ |__|_/ ____\___.__. 
|    |  \   Y   /_/ __ \\_  __ \|  |\   __\<   |  |    
|    |___\     / \  ___/ |  | \/|  | |  |   \___  |     
|_______ \\___/   \___  >|__|   |__| |__|   / ____| 
        \/            \/ [ By // lalaio1 ]  \/      
                                                      
"""
    print(f"{cor_azul} {cor_roxa} {banner}{cor_reset}")


if __name__ == "__main__":
    os.system("clear" if os.name != "nt" else "cls")

    flag_status = verificar_e_definir_flag()

if flag_status == "True":
    print(f"{cor_azul}[{cor_verde}+{cor_azul}] Verificação já foi executada anteriormente. Saindo...{cor_reset}")
    os.system("clear" if os.name != "nt" else "cls")
    if os.name != "posix":
        os.system("python ./conf/scripts/start2.py")
        
else:
    imprimir_banner()
    instalar_bibliotecas_necessarias()
    setar_flag_true()
    print(f"{cor_azul}[{cor_verde}!{cor_azul}] Bibliotecas instaladas. Verificação concluída.{cor_reset}")
    if os.name != "posix":
        os.system("python ./conf/scripts/start2.py")