import PyInstaller.__main__
import os

# Functions
__all__ = ['create_app']

# Variables
__all__ += []

def create_executable(script_name, executable_name, release_dir='release', icon_path=None, no_console=False):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_path = os.path.join(current_dir, script_name)

    if not os.path.exists(main_py_path):
        print(f"'{script_name}' não encontrado.")
        return

    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    pyinstaller_command = [
        main_py_path,
        '--onefile',
        f'--distpath={release_dir}',
        f'--name={executable_name}',
        f'--specpath={release_dir}'
    ]

    if icon_path:  # Adiciona o caminho do ícone se fornecido
        pyinstaller_command.append(f'--icon={icon_path}')
    
    if no_console:  # Adiciona a opção noconsole se verdadeiro
        pyinstaller_command.append('--noconsole')

    PyInstaller.__main__.run(pyinstaller_command)

def create_app(script_path: str, exe_name: str, release_dir_path: str, icon_path=None, no_console=False):
    script_to_convert = script_path
    executable_name = exe_name
    release_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), release_dir_path)
    create_executable(script_to_convert, executable_name, release_dir, icon_path, no_console)

if __name__ == "__main__":
    pass
