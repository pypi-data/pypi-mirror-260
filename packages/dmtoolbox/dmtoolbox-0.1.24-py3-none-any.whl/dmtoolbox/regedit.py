import winreg

if __package__ is None or __package__ == '':
    from dmtoolbox.osFuncs import *
else:
    from .osFuncs import *
    
    
# Functions
__all__ = ['is_protocol_reg_created', 'register_protocol', 'check_and_create_protocol_reg']

# Variables
__all__ += []


def is_protocol_reg_created(protocol_name):
    try:
        # Try to open the registry key
        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, protocol_name)
        
        # If the key exists, close it and return True
        winreg.CloseKey(registry_key)
        return True
    except FileNotFoundError:
        # If the key does not exist, return False
        return False

def register_protocol(protocol_name, executable_path):
    if not is_admin():
        raise PermissionError("Este programa precisa ser executado com privilégios de administrador.")

    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, protocol_name) as key:
        winreg.SetValue(key, '', winreg.REG_SZ, f'URL:{protocol_name} Protocol')
        winreg.SetValueEx(key, 'URL Protocol', 0, winreg.REG_SZ, '')

    with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f'{protocol_name}\\shell\\open\\command') as key:
        winreg.SetValue(key, '', winreg.REG_SZ, f'"{executable_path}" "%1"')

def check_and_create_protocol_reg(protocol_name, executable_path): 
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, protocol_name):
            pass
    except FileNotFoundError:
        register_protocol(protocol_name, executable_path)


if __name__ == "__main__":
    print("Este módulo não deve ser executado diretamente.")



