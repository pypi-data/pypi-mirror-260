import PyInstaller.__main__
import os

# Functions
__all__ = ['create_app']

# Variables
__all__ += []

def create_executable(script_name, executable_name, release_dir='release'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_path = os.path.join(current_dir, script_name)

    if not os.path.exists(main_py_path):
        print(f"'{script_name}' não encontrado.")
        return

    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    PyInstaller.__main__.run([
        main_py_path,
        '--onefile',
        # '--noconsole',
        f'--distpath={release_dir}',
        f'--name={executable_name}',
        f'--specpath={release_dir}',
        '--icon=C:/Users/corsh/OneDrive/Documentos/Facul/Away/Repositórios/Gerenciador de Arquivos com servidor local/public/assets/file-explorer.ico',

    ])

def create_app(script_path: str, exe_name: str, release_dir_path: str):
    
    script_to_convert = script_path
    executable_name = exe_name
    release_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), release_dir_path)
    create_executable(script_to_convert, executable_name, release_dir)


        
if __name__ == "__main__":
    pass
    

        
