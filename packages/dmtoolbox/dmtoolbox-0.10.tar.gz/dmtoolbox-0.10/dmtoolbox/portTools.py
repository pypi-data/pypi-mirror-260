from colorama import Fore, Style, init
import random
import json
import os
import subprocess

if __package__ is None or __package__ == '':
    from dmtoolbox.osFuncs import *
    from dmtoolbox.appdataGen import *
else:
    from .osFuncs import *
    from .appdataGen import *



# Functions
__all__ = ['check_port_availability', 'find_available_ports', 'find_port', 'setup_available_port']

# Variables
__all__ += ['PREFERRED_PORTS', 'AVAILABLE_PORT']


PREFERRED_PORTS = [
    49200,
    49300,
    49400,
    49500,
    49600,
    49700,
    49800,
    49900,
    50100,
    50200 
]

AVAILABLE_PORT = PREFERRED_PORTS[0]

init() 

def check_port_availability(port, host='127.0.0.1'):
    # Primeiro, encontra o PID usando a porta
    command_find_pid = f'netstat -aon | findstr /R /C:"{host}:{port}"'
    result_find_pid = subprocess.run(command_find_pid, capture_output=True, text=True, shell=True)

    if result_find_pid.stdout:
        # Extrai o PID da saída
        lines = result_find_pid.stdout.strip().split('\n')
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 4 and parts[1] == f'{host}:{port}':
                pid = parts[-1]  # O PID é geralmente o último elemento
                
                # Usa tasklist para encontrar o nome do processo usando o PID
                command_find_process = f'tasklist /FI "PID eq {pid}"'
                result_find_process = subprocess.run(command_find_process, capture_output=True, text=True, shell=True)
                
                if "nginx" in result_find_process.stdout.lower() or "DMFILEExplorer.exe" in result_find_process.stdout.lower():
                    # Se o processo for Nginx ou Flask, trata a porta como disponível
                    return True

        # Se chegou até aqui, a porta está em uso, mas não por Nginx ou Flask
        return False
    else:
        # A porta está disponível
        return True
    
    
def find_available_ports(start_port, end_port, host='127.0.0.1'):
    """
    Encontra portas disponíveis em um dado range.

    :param start_port: Início do intervalo de portas a ser verificado.
    :param end_port: Fim do intervalo de portas a ser verificado.
    :param host: Endereço IP para verificar a disponibilidade das portas. Padrão é '127.0.0.1'.
    :return: Lista de portas disponíveis no intervalo especificado.
    """
    available_ports = []
    for port in range(start_port, end_port + 1):
        if check_port_availability(port, host):
            available_ports.append(port)
    return available_ports

def find_port_internal(preferred_ports=PREFERRED_PORTS):
    
    # Etapa 1: Verificar portas pré-definidas
    for port in preferred_ports:
        if check_port_availability(port):
            return port

    # Etapa 2: Testar 100 portas aleatórias
    try:
        random_ports = random.sample(range(49152, 65536), 100)
    except ValueError:
        # Caso a geração de portas aleatórias falhe devido ao range ser pequeno
        random_ports = range(49152, 65536)
    
    for port in random_ports:
        if check_port_availability(port):
            return port

    # Etapa 3: Testar todas as portas no intervalo, se necessário
    for port in range(49152, 65536):
        if check_port_availability(port):
            return port

    # Se nenhuma porta disponível for encontrada, lança uma exceção personalizada
    raise Exception("Não foi possível encontrar uma porta disponível. Verifique a configuração da rede.")

def find_port():
    
    try:
        return find_port_internal()
    except Exception as e:
        print(Fore.RED + f"Erro: {e}" + Style.RESET_ALL)
    
# def setup_available_port():
#     global METADATA
#     metadata_file = METADATA
#     metadata = {}

#     # Verifica se o arquivo METADATA já existe e lê seu conteúdo
#     if os.path.exists(metadata_file):
#         with open(metadata_file, 'r') as file:
#             try:
#                 metadata = json.load(file)
#             except json.JSONDecodeError:
#                 metadata = {}

#     # Verifica se 'AVAILABLE_PORT' está em 'metadata'
#     if 'AVAILABLE_PORT' in metadata:
#         if check_port_availability(metadata['AVAILABLE_PORT']):
#             # A porta armazenada está disponível
#             return metadata['AVAILABLE_PORT']
#         else:
#             # A porta armazenada não está disponível, encontra uma nova
#             new_port = find_port()
#     else:
#         # 'AVAILABLE_PORT' não está em 'metadata', encontra uma nova
#         new_port = find_port()

#     # Atualiza 'metadata' com a nova porta disponível e salva no arquivo
#     metadata['AVAILABLE_PORT'] = new_port
    
#     if not os.path.exists(metadata_file):
#         create_appdata()
    
#     with open(metadata_file, 'w') as file:
#         json.dump(metadata, file, indent=4)
    
#     return new_port

# TODO Ajeitar a função para dar imput na porta para o nginx e para o servidor flask

def setup_available_port():
    return 49200



if __name__ == '__main__':
    pass


