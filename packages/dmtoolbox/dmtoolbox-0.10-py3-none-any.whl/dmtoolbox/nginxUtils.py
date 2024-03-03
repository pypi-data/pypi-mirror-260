
import subprocess
import os
import re

if __package__ is None or __package__ == '':
    from dmtoolbox.portTools import *
    from dmtoolbox.nginxDefaults import *
    from dmtoolbox.osFuncs import *
    from dmtoolbox.appdataGen import *
else:
    from .portTools import *
    from .nginxDefaults import *
    from .osFuncs import *
    from .appdataGen import *
    
    

    
# Functions
__all__ = ['start_nginx', 'stop_nginx', 'is_nginx_running', 'setup_nginx']


# Variables
__all__ += ['NGINX_ROOT_PATH']

    

# MODIFY
# Estou setando o caminho aqui na pasta do projeto, mas ao levar pra prod modificar para standard
NGINX_ROOT_PATH = os.path.join(APPDATA_DIR, 'nginx-1.24.0')
NGINX_CONF_PATH = os.path.join(NGINX_ROOT_PATH, 'conf', 'nginx.conf')


FOUND_DIRECTIVES = {}


def start_nginx():
    """
    Inicia o servidor Nginx.

    Args:
        nginx_root_path (str): O caminho raiz do Nginx.

    Returns:
        bool: True se o Nginx foi iniciado com sucesso, False caso contrário.
    """
    if is_nginx_running():
        return 
    
    print("Iniciando servidor de proxy reverso...")
    
    global NGINX_ROOT_PATH
    global AVAILABLE_PORT
    
    nginx_root_path = NGINX_ROOT_PATH

    nginx_exe_path = os.path.join(nginx_root_path, 'nginx.exe')
    nginx_command = f'"{nginx_exe_path}"'

    # Executar o comando usando subprocess
    try:
        subprocess.Popen(nginx_command, cwd=nginx_root_path)
        print(f"Servidor de proxy reverso iniciado com sucesso na porta {AVAILABLE_PORT}")
        return True
    except Exception as e:
        print(f"Erro ao iniciar o Nginx: {e}")
        return False

def stop_nginx():
    if is_nginx_running():
        raise_admin()
        print("Encerrando servidor de proxy reverso...")

        global NGINX_ROOT_PATH
        
        # Comando para encerrar o Nginx
        nginx_command = 'taskkill /F /IM nginx.exe'

        # Executar o comando usando subprocess
        try:
            subprocess.run(nginx_command, shell=True, check=True)
            print("Servidor de proxy reverso encerrado com sucesso")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao encerrar o Nginx: {e}")
            
    else:
        return

def restart_nginx():
    print("Iniciando processo de reinicialização do servidor de proxy reverso...")

    if is_nginx_running():
        stop_nginx()
        
    start_nginx()
    
    print("Processo de reinicialização do servidor de proxy reverso finalizado com sucesso...")
        
def is_nginx_running():
    try:
        # Executa o comando 'tasklist' para listar os processos em execução
        output = subprocess.check_output('tasklist', shell=True, text=True)
        # Verifica se 'nginx.exe' está na saída
        return 'nginx.exe' in output
    except subprocess.CalledProcessError:
        # Em caso de erro ao chamar o processo, assume que o Nginx não está em execução
        return False
     
def check_nginx_config():
    global HOST_MAPPING
    global NGINX_CONF_PATH
    global AVAILABLE_PORT
    
    hostname = HOST_MAPPING
    nginx_conf_path = NGINX_CONF_PATH
    available_port = AVAILABLE_PORT
    
    if not os.path.exists(nginx_conf_path):
        return { 'error': False }

    found_directives = {
        'listen': False,
        'server_name': False,
        'proxy_pass': False,
        'proxy_set_header Host': False,
        'proxy_set_header X-Real-IP': False,
        'proxy_set_header X-Forwarded-For': False,
        'proxy_set_header X-Forwarded-Proto': False
    }

    try:
        with open(nginx_conf_path, 'r') as f:
            for line in f:
                line = line.strip()
                for directive in found_directives:
                    if directive in line:
                        # Procura pela diretiva e o argumento na linha
                        argument = re.findall(rf'{directive}\s+([^;]+)', line)
                        if argument:
                            if directive == 'listen' and '80' in argument[0]:
                                found_directives[directive] = True
                            elif directive == 'server_name' and hostname in argument[0]:
                                found_directives[directive] = True
                            elif directive == 'proxy_pass':
                                proxy_port_match = re.search(r'http://\d+\.\d+\.\d+\.\d+:(\d+);', line)
                                if proxy_port_match and proxy_port_match.group(1) == str(available_port):
                                    found_directives[directive] = True
                            
                            else:
                                found_directives[directive] = True

    except IOError as e:
        print(f"Erro ao ler o arquivo de configuração: {e}")
        
    return found_directives

def is_nginx_configured():
    global FOUND_DIRECTIVES
    
    FOUND_DIRECTIVES = check_nginx_config()
    
    # Verifica se todas as configurações necessárias foram encontradas
    if all(FOUND_DIRECTIVES.values()):
        return True
    
    else:
        return False

def is_nginx_default_config():
    global NGINX_CONF_PATH
    global NGINX_WIN_DEFAULT
    
    return is_actual_Config_iquals_expected(NGINX_WIN_DEFAULT, NGINX_CONF_PATH)

def is_nginx_util_config():
    global NGINX_CONF_PATH
    global NGINX_UTIL
    
    return is_actual_Config_iquals_expected(NGINX_UTIL, NGINX_CONF_PATH)

def is_actual_Config_iquals_expected(expected_config, path_file):
    
    try:
        with open(path_file, 'r') as file:
            content = file.read()
            return content.strip() == expected_config.strip()
    except FileNotFoundError:
        print(f"O arquivo '{path_file}' não foi encontrado.")
        return False
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo '{path_file}': {e}")
        return False

def is_nginx_blank_config():
    # Verifica se a configuração do NGINX está vazia
    return not NGINX_UTIL.strip()  # Se a configuração estiver vazia, retorna True; caso contrário, retorna False

def create_nginx_util_config():
    global NGINX_CONF_PATH
    global NGINX_UTIL
    
    nginx_conf_path = NGINX_CONF_PATH


    try: 

        with open(nginx_conf_path, 'w') as f:
            f.write(NGINX_UTIL)

    except IOError as e:
        print(f"Erro ao ler ou escrever no arquivo de configuração: {e}")

def setup_nginx():    
    if not is_nginx_configured():
        print("\nConfigurando servidor de proxy reverso...")
        
        if is_nginx_default_config() or is_nginx_blank_config():
            create_nginx_util_config()
            restart_nginx()
        
        else:
            # MODIFY
            # AQUI Estou setando o create, mas é necessario fazer a tratativa caso o usuario tenha configs no nginx
            create_nginx_util_config()
            restart_nginx()
            
        
        if not is_nginx_util_config():
            # MODIFY
            # AQUI Estou setando o create, mas é necessario fazer a tratativa caso o usuario tenha configs no nginx
            create_nginx_util_config()
            restart_nginx()
        
        print("Servidor de proxy reverso configurado com sucesso.")
    
    start_nginx()
    

        
        
    



if __name__ == '__main__':
    pass
    

