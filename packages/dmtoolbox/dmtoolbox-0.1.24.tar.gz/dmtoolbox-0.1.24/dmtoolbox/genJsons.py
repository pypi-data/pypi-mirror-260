
import os
import json
import re

    
# Functions
__all__ = ['file_to_json', 'save_json_to_json_file', 'update_variable_declaration_in_script']

# Variables
__all__ += []



def file_to_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return None

def save_json_to_json_file(json_content, file_path):
    # Garantindo que o diretório onde o arquivo será salvo existe
    os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # json.dump é usado para converter o objeto Python (dicionário ou lista) em JSON e salvar no arquivo
            json.dump(json_content, file, indent=4, ensure_ascii=False)
        print(f"Arquivo JSON salvo com sucesso em: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

def update_variable_declaration_in_script(file_path, script_path, variable_name):
    try:
        # Abre o arquivo que contém a string JSON e lê seu conteúdo
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo '{file_path}': {e}")
        return

    # Prepara o novo conteúdo a ser inserido no script de destino
    new_declaration = f'{variable_name} = {content}\n'

    try:
        with open(script_path, 'r', encoding='utf-8') as original_script:
            lines = original_script.readlines()

        # Substitui a declaração da variável no script
        updated_lines = []
        variable_pattern = re.compile(f'^{variable_name} =')
        for line in lines:
            if variable_pattern.match(line):
                updated_lines.append(new_declaration)
            else:
                updated_lines.append(line)

        with open(script_path, 'w', encoding='utf-8') as modified_script:
            modified_script.writelines(updated_lines)

        print(f"Declaração da variável '{variable_name}' atualizada com sucesso no script '{script_path}'.")
    except FileNotFoundError:
        print(f"Erro: Script de destino '{script_path}' não encontrado.")
    except Exception as e:
        print(f"Erro ao modificar o script '{script_path}': {e}")


    
if __name__ == '__main__':
    pass
