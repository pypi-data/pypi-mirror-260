import os
import ctypes
import platform
import sys
import os
import shutil




# Functions
__all__ = ['get_script_directory', 'is_admin', 'raise_admin', 'is_installed', 'write_file', 'copy_file', 'verify_dependencies']

# Variables
__all__ += ['DIR_PATH', 'PKG_DEPENDENCIES']

PKG_DEPENDENCIES = ['pandas', 'openpyxl', 'jinja2', 'numpy', 'prettytable', 'colorama', 'pyinstaller']


def get_script_directory():
    """
    Retorna o diretório do script atual, funcionando tanto para scripts Python
    executados diretamente quanto para executáveis gerados pelo PyInstaller.
    """
    if getattr(sys, 'frozen', False):
        # Caminho do executável quando o script é empacotado pelo PyInstaller.
        script_directory = os.path.dirname(sys.executable)
    else:
        # Caminho normal quando o script é executado como um script Python.
        script_directory = os.path.dirname(os.path.abspath(__file__))
    return script_directory

DIR_PATH = get_script_directory()

def is_admin():
    os_name = platform.system()
    
    if os_name == 'Windows':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:  # Isso cobrirá Linux, Darwin (macOS) e outras variantes Unix
        try:
            return os.getuid() == 0
        except AttributeError:
            return False
    
def raise_admin():
    if not is_admin():
        os_name = platform.system()
        if os_name == 'Windows':
            # Solicita elevação de privilégios e reinicia o script no Windows
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(f'"{arg}"' for arg in sys.argv), None, 1)
            sys.exit(0)
        else:
            # Para sistemas não Windows, instrui o usuário a reiniciar o script com privilégios elevados
            print("Este script precisa ser executado com privilégios de administrador. Por favor, reinicie o script usando 'sudo' (Linux/macOS).")
            sys.exit(1)      

def is_installed(destination, filename):
    # Checks if the file exists in the destination directory
    full_path = os.path.join(destination, filename)
    return os.path.exists(full_path)

def write_file(new_file_content, file_path, overwrite=True):
   
    if overwrite:    
        with open(file_path, 'w', encoding='utf-8') as file:  # Adiciona 'encoding="utf-8"'
            file.write(new_file_content)
    else: 
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            
        file_content += new_file_content
        
        with open(file_path, 'w', encoding='utf-8') as file:  # Adiciona 'encoding="utf-8"'
            file.write(file_content)

def copy_file(origin, destination, new_filename=None):
    """
    Copia um arquivo de 'origin' para 'destination', permitindo a mudança do nome do arquivo de destino.

    :param origin: O caminho completo do arquivo de origem.
    :param destination: O diretório de destino para o arquivo.
    :param new_filename: Novo nome para o arquivo no destino (opcional).
    """
    try:
        # Certifica-se de que o diretório de destino existe, cria se necessário
        os.makedirs(destination, exist_ok=True)

        # Define o caminho completo do destino incluindo o novo nome do arquivo, se fornecido
        if new_filename:
            destination_path = os.path.join(destination, new_filename)
        else:
            destination_path = os.path.join(destination, os.path.basename(origin))
        
        # Copia o arquivo
        shutil.copyfile(origin, destination_path)
        print(f"Arquivo copiado para '{destination_path}' com sucesso.")
    except FileNotFoundError:
        print(f"Erro: O arquivo de origem '{origin}' não foi encontrado.")
    except PermissionError:
        print("Erro de permissão: Não foi possível copiar o arquivo. Verifique as permissões.")
    except Exception as e:
        print(f"Erro ao copiar o arquivo: {e}")

def verify_dependencies(dependencies=[], to_verify=''):
    
    if to_verify == '':
        required_modules = dependencies
    elif to_verify == 'pkg':
        required_modules = PKG_DEPENDENCIES
    else:
        print('Comando não reconhecido, verifique o arguemento "to_verify"')
        return None
    
    
    
    for mod in required_modules:
        try:
            __import__(mod)
        except ModuleNotFoundError:
            print(f'\nErro: O módulo "{mod}" é necessário mas não foi encontrado.')
            print(f'Por favor, instale o "{mod}" executando: pip install {mod}\n')
            return False
    return True


if __name__ == '__main__':
    pass
