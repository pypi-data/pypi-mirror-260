import os
import json
import ctypes
import sys


if __package__ is None or __package__ == '':
    from dmtoolbox.osFuncs import *
else:
    from .osFuncs import *
    

# Functions
__all__ =  ['create_appdata_folder', 'create_appdata_inner_folder', 'save_json_to_file', 'create_file_in_directory']


# Variables
__all__ += ['METADATA_PATH', 'APPDATA_FOLDER_PATH', 'APPDATA_DIR'] 



APPDATA_DIR = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'LocalLow')



APPDATA_FOLDER_DIR = 'test-name'
APPDATA_FOLDER_PATH = os.path.join(APPDATA_DIR, APPDATA_FOLDER_DIR)
METADATA_PATH = os.path.join(APPDATA_FOLDER_PATH, 'metadata', 'metadata.json')



def create_appdata_folder(folder_name):
    global APPDATA_DIR
    print(f"==>> APPDATA_DIR: {APPDATA_DIR}")
    
    # Cria o caminho completo para a nova pasta dentro do AppData
    new_folder_path = os.path.join(APPDATA_DIR, folder_name)
    # Verifica se a pasta já existe para evitar a criação duplicada
    if not os.path.exists(new_folder_path):
        
        if not is_admin():
            # Solicita elevação de privilégios e reinicia o script
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(map(str, sys.argv)), None, 1)
            sys.exit(0)
            
        try:
            # Cria a pasta
            os.makedirs(new_folder_path)
            print(f"A pasta '{new_folder_path}' foi criada com sucesso.")
        except Exception as e:
            print(f"Não foi possível criar a pasta: {e}")     

def create_appdata_inner_folder(folder_name):
    global APPDATA_FOLDER_PATH
    
    # Cria o caminho completo para a nova pasta dentro do AppData
    new_folder_path = os.path.join(APPDATA_FOLDER_PATH, folder_name)
    
    # Verifica se a pasta já existe para evitar a criação duplicada
    if not os.path.exists(new_folder_path):
        try:
            # Cria a pasta
            os.makedirs(new_folder_path)
            print(f"A pasta '{new_folder_path}' foi criada com sucesso.")
        except Exception as e:
            print(f"Não foi possível criar a pasta: {e}")

def save_json_to_file(json_content, file_path):
    # Verifica se o arquivo já existe
    if os.path.exists(file_path):
        return

    # Garantindo que o diretório onde o arquivo será salvo existe
    os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # Se json_content já for uma string formatada, escreva diretamente
            if isinstance(json_content, str):
                file.write(json_content)
            # Se json_content for um dicionário, converta para JSON e salve
            else:
                json.dump(json_content, file, indent=4, ensure_ascii=False)
        print(f"Arquivo JSON salvo com sucesso em: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

def create_file_in_directory(directory_path, file_name, content=None):
    
    file_path = os.path.join(directory_path, file_name)
    try:
        if os.path.exists(file_path):
            return
        with open(file_path, 'w', encoding='utf-8') as file:
            if content:
                file.write(content)
        print(f"Arquivo '{file_name}' criado com sucesso em: {directory_path}")
    except Exception as e:
        print(f"Erro ao criar o arquivo '{file_name}' em '{directory_path}': {e}")

def create_directory(directory_path):
    """Cria um diretório se ele não existir."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Diretório criado: {directory_path}")

def save_content_to_file(content, file_path):
    """Salva conteúdo em um arquivo, substituindo-o se já existir."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Conteúdo salvo em: {file_path}")
