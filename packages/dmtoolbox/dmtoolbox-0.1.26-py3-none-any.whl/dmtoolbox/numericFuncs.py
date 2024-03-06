#  ===============================================================================
#
#  Autor: Daniel Mello
#  Data: 28/02/2024
#  
#  Objetivo do script:
#  Este script contém uma coleção de funções e utilitários matemáticos e de manipulação de dados em Python.
#  Ele oferece funcionalidades como operações matriciais, formatação de dados, exportação para Excel e plotagem de gráficos.
#  O script foi projetado para ser reutilizável e modular, facilitando sua integração em diversos projetos.
#
#  
#  Nome: dmtoolbox
#  Este script foi projetado para ser importado como um módulo chamado "dmtoolbox", que contém diversas funções 
#  úteis para operações matemáticas e manipulação de dados.
#
#
#  Obs:
#  - Certifique-se de que as dependências listadas no início do script estão instaladas para garantir o funcionamento correto.
#  - Algumas funções podem exigir determinadas versões ou configurações específicas das bibliotecas de terceiros importadas.
#
#
#  ===============================================================================



import pandas as pd
import numpy as np
from prettytable import PrettyTable
from datetime import datetime
import matplotlib.pyplot as plt
import inspect

if __package__ is None or __package__ == '':
    from dmtoolbox.osFuncs import *
else:
    from .osFuncs import *

# Functions
__all__ = [
    'printMatrizNN',
    'printVetor',
    'separador',
    'insereMudancaLinha',
    'mat_transpose',
    'mult_matrizes',
    'round_nf',
    'count_d_places',
    'createFile',
    'export_to_excel',
    'plot_2d_function_and_compare',
    'plot_3d_function_and_arrows',
    'plot_and_compare'
]


# Variables
__all__ += ['NUMERIC_DEPENDENCIES']


NUMERIC_DEPENDENCIES = ['pandas', 'openpyxl', 'jinja2']


# ========== #
#  Formatar  #
# ========== #

def printMatrizNN (mat, headers='', transpose=True):
        
    data=mat
    
    table = PrettyTable()
    
    if headers == '':
        table.header = False
        
    elif headers != '':
        table.field_names = headers
        
    if transpose:
        data = mat_transpose(mat)    


    for linha in data:
        table.add_row(linha)
            
    print(table)    
    
def printVetor(list_: list):

    print('[', end='')
    for i in range(len(list_)):
        if i != len(list_) - 1:
            print(f'{list_[i]}, ', end='')
        else:
            print(f'{list_[i]}', end='')
    print(']')

def separador (matriz: list, tag):
    
    linhaVazia = [''] * 10
    
    matriz.append(linhaVazia)
    matriz.append(tag)
    matriz.append(linhaVazia)

def insereMudancaLinha (matriz: list, linhas: tuple):
 
    linhaVazia = [''] * 10
    #refatorar
    
    texto = ['A linha {} trocou de lugar com a linha {}   {}'.format(linhas[0], linhas[1], linhas)]
    
    matriz.append(linhaVazia)
    matriz.append (texto)
    matriz.append(linhaVazia)

def mat_transpose(mat: list, method='np'):
    
    match method:
        case 'np':
            return (np.array(mat, dtype='object').T).tolist()
        
        case 'map':
            return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]
        
        case 'zip':
            return list(map(list, zip(*mat)))


# ====================== #
#  Operações Matriciais  #
# ====================== #
     
def mult_matrizes(matriz1, matriz2):
    
    if len(matriz1[0]) != len(matriz2):
        raise ValueError("O número de colunas da matriz 1 deve ser igual ao número de linhas da matriz 2.")
    
    
    result = [[0 for _ in range(len(matriz2[0]))] for _ in range(len(matriz1))]
    
    
    for i in range(len(matriz1)): 
        for j in range(len(matriz2[0])): 
            for k in range(len(matriz2)): 
                
                result[i][j] += matriz1[i][k] * matriz2[k][j] 
    
    return result


# ===================== #
#  Funções matemáticas  #
# ===================== #

def round_nf(number=None, d_places=0, method='default', alt='default'):


    if alt == 'exib':
        return number, round_nf(number, d_places, method=method)
        
                
    elif alt =='default':
        match method:
            case 'default':
                return round(number, d_places)
            
            case '':
                return round(number, d_places)
            
            case 'trunc':
                
                if d_places == 0:
                    return int(number)
                
                return float( str(number)[:str(number).find('.') + d_places+1] )
            case 'noround':
                return number
            
            case _:
                raise ValueError(f"Unknown rounding method: {method}")

def count_d_places(number):
    """
    Conta o número de casas decimais de um número.

    Parâmetros:
    - numero (float): O número do qual as casas decimais serão contadas.

    Retorna:
    - int: O número de casas decimais.
    """
    # Convertendo o número para string
    number_str = str(number)
    
    # Verificando se o número tem uma parte decimal
    if '.' in number_str:
        # Contando os caracteres após o ponto decimal
        return len(number_str.split('.')[1])
    else:
        # Se não há parte decimal, retorna 0
        return 0


# ===================== #
#  Funções de arquvios  #
# ===================== #

def createFile(dataFrame: pd.DataFrame, file_name, file_path='./', index=False):
    
    complete_name = file_path + file_name + '.xlsx'
    try:    
        dataFrame.to_excel(complete_name, engine='openpyxl', index=index)
        return True
        
    except PermissionError as e:
        error_message = str(e)
        
        if 'file is being used by another process' in error_message or 'Permission denied' in error_message:
            print(f'\n\n AVISO: Permissão negada para sobrescrever o arquivo : \'{complete_name}\'.')
            print('Verifique se o arquivo que está tentando criar já existe e está sendo utilizado por outro programa.')
            print('Se não for o caso verifique se essa pasta foi definida com workspace trust, ', end='')
            print ('para garantir que tem permissão para modificar arquivos.\n')
            print(f'** Erro retornado: {error_message}  **\n\n')
        
            print('Opções:')
            print('1. Escolher um nome de arquivo diferente.')
            print('2. Confirmar a substituição do arquivo existente (caso o arquivo não esteja mais sendo utilizado).')
            print('3. Cancelar a operação.')
            escolha = input('\nDigite o número da opção desejada: ')
                  
            if escolha == '1':
                novo_nome = input('Digite um novo nome de arquivo sem extensões: ')
                createFile(dataFrame, (novo_nome + '.xlsx'), index=index)
                
                return True
                
            elif escolha == '2':
                createFile(dataFrame, file_name, index=index)
                
                return True
            
            elif escolha == '3':
                         
                return False
            else:
                print('\nOpção inválida. Tente novamente.')
  
def export_to_excel(mat, path='./', caption=None, transpose = False, headers=None, file_name='test-'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")):
    
    if not verify_dependencies(NUMERIC_DEPENDENCIES):
        return  # Alguma dependência está faltando, então a função termina aqui
    
    if transpose:
        df = pd.DataFrame(mat).T
    else:
        df = pd.DataFrame(mat)
        
    # Definir cabeçalhos personalizados se fornecidos
    if headers is not None:
        df.columns = headers
    
    # Se uma legenda foi fornecida, aplicar estilo e definir a legenda
    if caption:
        styler = df.style
        if caption:
            styler = styler.set_caption(caption)

        styler = styler.set_properties(**{'text-align': 'center'})
        
        
    
    # Exportação do DataFrame para um arquivo Excel
    while True:
        
        try:
            if caption:
                return createFile(styler, file_name, path)
            elif not caption:
                return createFile(df, file_name, path)

            break
        
        except Exception as e:
            
            print(f'\nErro ao salvar o arquivo: {e}')
            input('\nNão é possível sobrescrever o arquivo! Feche o arquivo caso esteja aberto e tente novamente...\n')
    
    pass


# ================ #
#  Plot Functions  #
# ================ #


def plot_2d_function_and_compare(ydx, x_range, x_points, y_points, angles, arrow_length=0.2, rad=True):

    x_values = np.linspace(x_range[0], x_range[1], 400)
    y_values = [ydx(x) for x in x_values]

    # Plotar a curva da função
    plt.plot(x_values, y_values, label='Curva da função fdxy', zorder=1)

    # Plotar os pontos dados
    plt.scatter(x_points, y_points, color='red', zorder=5, label='Pontos dados')

    # Para cada ponto e ângulo dados, plotar uma seta com o ângulo dado
    for xi, yi, angle in zip(x_points, y_points, angles):
        # Converter ângulo para radianos se necessário
        angle_rad = angle if rad else np.deg2rad(angle)

        # Calcular o vetor direção normalizado (comprimento 1)
        dx = np.cos(angle_rad)
        dy = np.sin(angle_rad)

        # Normalizar o vetor direção (dx, dy)
        length = np.sqrt(dx**2 + dy**2)
        dx /= length
        dy /= length

        # Plotar a seta com tamanho padrão
        plt.arrow(xi, yi, dx*arrow_length, dy*arrow_length, head_width=0.1, head_length=0.1, fc='black', ec='black', zorder=4)

        # Plotar a linha vertical pontilhada do ponto dado até a curva
        yi_true = ydx(xi)
        plt.vlines(xi, yi, yi_true, color='black', linestyles='dashed', zorder=4)

    # Adicionar legendas e títulos
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Comparação entre a função fdxy e pontos dados com setas em ângulos definidos')
    plt.legend()

    # Exibir o gráfico
    plt.show()

def plot_3d_function_and_arrows(ydx, x_range, y_range, x_points, y_points, z_points, angles, arrow_length=0.2, rad=True):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Gera uma grade de valores para x e y
    x_values = np.linspace(x_range[0], x_range[1], 400)
    y_values = np.linspace(y_range[0], y_range[1], 400)
    x_grid, y_grid = np.meshgrid(x_values, y_values)

    # Calcula os valores de z com base na função ydx para cada ponto na grade
    z_grid = ydx(x_grid, y_grid)

    # Plotar a superfície
    surf = ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', edgecolor='none', alpha=0.7)

    # Para cada ponto e ângulo dados, plotar uma seta
    for xi, yi, zi, angle in zip(x_points, y_points, z_points, angles):
        # Converter ângulo para radianos se necessário
        angle_rad = angle if rad else np.deg2rad(angle)

        # Calcular o vetor direção normalizado (comprimento 1)
        u = np.cos(angle_rad) * arrow_length
        v = np.sin(angle_rad) * arrow_length
        w = 0  # Sem componente vertical para as setas

        # Plotar a seta usando quiver
        ax.quiver(xi, yi, zi, u, v, w, length=arrow_length, arrow_length_ratio=0.1, color='black')

    # Adicionar legendas e títulos
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Gráfico 3D da função ydx e setas direcionais')

    # Exibir o gráfico
    plt.show()
    
    
def plot_and_compare(ydx, x_range, x_points, y_points, angles, arrow_length=0.2, rad=True, y_range = None, z_points = None):
    if get_number_of_arguments(ydx) == 1:
        return plot_2d_function_and_compare(ydx = ydx,
                                           x_range = x_range, 
                                           x_points = x_points,
                                           y_points = y_points,
                                           angles = angles,
                                           arrow_length=arrow_length,
                                           rad=rad
        )
    elif get_number_of_arguments(ydx) == 2:
        return plot_3d_function_and_arrows(ydx = ydx,
                                           x_range = x_range, 
                                           y_range = y_range,
                                           x_points = x_points,
                                           y_points = y_points,
                                           z_points = z_points,
                                           angles = angles,
                                           arrow_length=arrow_length,
                                           rad=rad
        )
    
    return print ('Função inválida utilziada')

def get_number_of_arguments(func):
    sig = inspect.signature(func)
    return len(sig.parameters)


if __name__ == '__main__':
    pass