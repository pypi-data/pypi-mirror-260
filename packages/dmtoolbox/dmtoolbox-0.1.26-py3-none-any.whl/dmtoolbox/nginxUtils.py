from abc import ABC, abstractmethod
import subprocess
import platform
import os
import re



if __package__ is None or __package__ == '':
    from dmtoolbox.portTools import *
    from dmtoolbox.nginxDefaults import *
    from dmtoolbox.osFuncs import *
    
else:
    from .portTools import *
    from .nginxDefaults import *
    from .osFuncs import *

    
    

    
# Functions
__all__ = ['start_nginx', 'stop_nginx', 'is_nginx_running', 'setup_nginx', 'nginx_controller']


# Variables
__all__ += ['NGINX_ROOT_PATH', 'DEFAULT_DIRECTIVES_EX1', 'DEFAULT_DIRECTIVES_IP', 'DEFAULT_NGINX_CONTENT_IP', 'DEFAULT_NGINX_CONTENT_EX1']


# Classes
__all__ += ['NginxController', 'WindowsNginxController', 'LinuxNginxController']




DEFAULT_DIRECTIVES_EX1 = {
    'listen': '80',
    'server_name': 'localhost',
    'proxy_pass': lambda value: value.startswith('http://127.0.0.1:'),
    'proxy_set_header Host': '$host',
    'proxy_set_header X-Real-IP': '$remote_addr',
    'proxy_set_header X-Forwarded-For': '$proxy_add_x_forwarded_for',       
    'proxy_set_header X-Forwarded-Proto': '$scheme',
}

DEFAULT_DIRECTIVES_IP = {
    'listen': '80 default_server',
    'listen': '[::]:80 default_server',
    'proxy_pass':lambda value: value.startswith('http://127.0.0.1:')
}

DEFAULT_NGINX_CONTENT_IP = """
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        
        location / {
            proxy_pass http://127.0.0.1:5000;
        }
    }
"""

DEFAULT_NGINX_CONTENT_EX1 = """
    server {
        listen 80;
        server_name localhost;
        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
"""


class NginxController(ABC):
    """
    Classe abstrata responsável por definir operações comuns e a interface para controle do servidor NGINX em diferentes sistemas operacionais.

    Atributos:
    -----------
    - CONSOLE_OUT_ALL : bool
        - Indica se todas as saídas do console devem ser exibidas. Utilizado para depuração.
    - QUIET_NGINX : bool
        - Determina se o servidor NGINX deve operar em modo silencioso, sem logar mensagens excessivas.
    - FOUND_DIRECTIVES : dict
        - Armazena as diretivas encontradas durante a verificação da configuração do NGINX.
    """
    CONSOLE_OUT_ALL = True
    QUIET_NGINX = False
    FOUND_DIRECTIVES = {}

    def restart_nginx(self, noconsole=True):
        """
        Reinicia o servidor NGINX, parando e iniciando o serviço novamente. Utiliza os métodos abstratos 'stop_nginx' e 'start_nginx'.

        Parâmetros:
        -----------
        - noconsole : bool, opcional
            - Define se as saídas para o console devem ser suprimidas. O padrão é True.

        Retorno:
        --------
        - None
        """
        if not noconsole or self.CONSOLE_OUT_ALL:
            print("Iniciando processo de reinicialização do servidor de proxy reverso...")

        if self.is_nginx_running():
            self.stop_nginx()
            
        self.start_nginx()
        
        if not noconsole or self.CONSOLE_OUT_ALL:
            print("Processo de reinicialização do servidor de proxy reverso finalizado com sucesso...")

    def is_nginx_configured(self, directives={}):
        """
        Verifica se o servidor NGINX está configurado com as diretivas especificadas.

        Parâmetros:
        -----------
        - directives : dict
            - Dicionário contendo as diretivas de configuração do NGINX e seus valores esperados ou funções de validação.

        Retorno:
        --------
        - bool
            - Retorna True se todas as diretivas especificadas estiverem corretamente configuradas, False caso contrário.
        """        

        self.FOUND_DIRECTIVES = self.check_nginx_config(directives)
        
        # Verifica se todas as configurações necessárias foram encontradas
        if all(self.FOUND_DIRECTIVES.values()):
            return True
        
        else:
            return False
    
    def is_actual_Config_iquals_expected(self, expected_config, path_file):
        """
        Compara o conteúdo atual de um arquivo de configuração do NGINX com uma configuração esperada.

        Parâmetros:
        -----------
        - expected_config : str
            - A configuração esperada como uma string.
        - path_file : str
            - O caminho para o arquivo de configuração a ser verificado.

        Retorno:
        --------
        - bool
            - Retorna True se o conteúdo do arquivo corresponder à configuração esperada, False caso contrário.
        """        
        
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
        
    @abstractmethod
    def start_nginx(self):
        """
        Inicia o servidor NGINX. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - None
        """
        pass

    @abstractmethod
    def stop_nginx(self):
        """
        Para o servidor NGINX. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - None
        """
        pass

    @abstractmethod
    def is_nginx_running(self):
        """
        Verifica se o servidor NGINX está em execução. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - bool
            - Retorna True se o NGINX estiver em execução, False caso contrário.
        """
        pass

    @abstractmethod
    def is_nginx_blank_config(self):
        """
        Verifica se o arquivo de configuração do NGINX está em branco. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - bool
            - Retorna True se o arquivo de configuração estiver em branco, False caso contrário.
        """
        pass

    @abstractmethod
    def create_nginx_config(self):
        """
        Cria ou atualiza a configuração do servidor NGINX. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - None
        """
        pass

    @abstractmethod
    def create_default_nginx_config(self):
        """
        Cria uma configuração padrão para o servidor NGINX. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - None
        """
        pass

    @abstractmethod
    def is_nginx_default_config(self):
        """
        Verifica se o servidor NGINX está utilizando a configuração padrão. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - bool
            - Retorna True se a configuração atual for a padrão, False caso contrário.
        """
        pass

    @abstractmethod
    def setup_nginx(self):
        """
        Configura o servidor NGINX com parâmetros específicos. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - None
        """
        pass

    @abstractmethod
    def update_nginx_config(self):
        """
        Atualiza a configuração do servidor NGINX. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - None
        """
        pass

    @abstractmethod
    def find_tag_indices(self):
        """
        Localiza índices de tags específicas dentro do arquivo de configuração do NGINX. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - tuple
            - Retorna um par de índices (início, fim) das tags especificadas, ou (None, None) se as tags não forem encontradas.
        """
        pass

    @abstractmethod
    def check_nginx_config(self):
        """
        Verifica a configuração do servidor NGINX contra um conjunto de diretivas especificadas. Deve ser implementado por subclasses específicas do sistema operacional.

        Parâmetros:
        -----------
        - Nenhum

        Retorno:
        --------
        - dict
            - Retorna um dicionário indicando o status da verificação para cada diretiva especificada.
        """
        pass
    
    
class WindowsNginxController(NginxController):
    """
    Controlador específico para a gestão do NGINX no ambiente Windows. Esta classe estende NginxController,
    fornecendo implementações concretas para iniciar, parar e verificar o status do NGINX, além de gerenciar
    a configuração do servidor no Windows.
    """
    # MODIFY
    # Estou setando o caminho aqui na pasta do projeto, mas ao levar pra prod modificar para standard
    
    NGINX_ROOT_PATH = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'LocalLow', 'nginx-1.24.0')
    NGINX_CONF_PATH = os.path.join(NGINX_ROOT_PATH, 'conf', 'nginx.conf')
    

    def start_nginx(self, noconsole=True):
        """
        Inicia o servidor NGINX no Windows. Se o servidor já estiver rodando, a função retorna sem tomar nenhuma ação.
        
        Parâmetros:
        -----------
        - noconsole : bool, opcional
            - Define se a saída do console deve ser suprimida. Por padrão, é True.
            
        Retorno:
        --------
        - bool
            - Retorna True se o servidor NGINX for iniciado com sucesso, False em caso de falha.
        """
        if self.is_nginx_running():
            return
        
        if not noconsole or self.CONSOLE_OUT_ALL:
            print("Iniciando servidor de proxy reverso...")
        
        nginx_exe_path = os.path.join(self.NGINX_ROOT_PATH, 'nginx.exe')
        nginx_command = f'"{nginx_exe_path}"'

        try:
            subprocess.Popen(nginx_command, cwd=self.NGINX_ROOT_PATH)
            if not noconsole or self.CONSOLE_OUT_ALL:
                print(f"Servidor de proxy reverso iniciado com sucesso na porta {AVAILABLE_PORT}")
            return True
        except Exception as e:
            if not noconsole or self.CONSOLE_OUT_ALL:
                print(f"Erro ao iniciar o Nginx: {e}")
            return False

    def stop_nginx(self, noconsole=True):
        """
        Para o servidor NGINX no Windows, enviando um comando de término específico do sistema.
        
        Parâmetros:
        -----------
        - noconsole : bool, opcional
            - Define se as mensagens de console durante o encerramento devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """
        if not self.is_nginx_running():
            if not noconsole or self.CONSOLE_OUT_ALL:
                print("Nginx não está rodando.")
            return
        
        if not noconsole or self.CONSOLE_OUT_ALL:
            print("Encerrando servidor de proxy reverso...")

        nginx_command = 'taskkill /F /IM nginx.exe'

        try:
            subprocess.run(nginx_command, shell=True, check=True)
            if not noconsole or self.CONSOLE_OUT_ALL:
                print("Servidor de proxy reverso encerrado com sucesso")
        except subprocess.CalledProcessError as e:
            if not noconsole or self.CONSOLE_OUT_ALL:
                print(f"Erro ao encerrar o Nginx: {e}")

    def is_nginx_running(self):
        """
        Verifica se o NGINX está atualmente rodando no Windows, examinando a lista de processos ativos.
        
        Parâmetros:
        -----------
        - Nenhum
        
        Retorno:
        --------
        - bool
            - Retorna True se o NGINX estiver rodando, False caso contrário.
        """
        try:
            output = subprocess.check_output('tasklist', shell=True, text=True)
            return 'nginx.exe' in output
        except subprocess.CalledProcessError:
            return False

    def is_nginx_blank_config(self):
        """
        Verifica se o arquivo de configuração do NGINX está vazio no Windows.
        
        Parâmetros:
        -----------
        - Nenhum
        
        Retorno:
        --------
        - bool
            - Retorna True se o arquivo de configuração estiver vazio, False caso contrário.
        """
        try:
            with open(self.NGINX_CONF_PATH, 'r') as conf_file:
                return not conf_file.read().strip()
        except FileNotFoundError:
            return True
        except Exception as e:
            print(f"Erro ao verificar o arquivo de configuração: {e}")
            return False

    def create_nginx_config(self, config_content=DEFAULT_NGINX_CONTENT_EX1, noconsole=True):
        """
        Cria ou atualiza o arquivo de configuração do NGINX no Windows com um novo conteúdo.
        
        Parâmetros:
        -----------
        - config_content : str
            - Conteúdo de configuração para ser escrito no arquivo nginx.conf.
        - noconsole : bool, opcional
            - Define se as mensagens de console durante a criação da configuração devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """
        format_init_spacement ='    # ==================== #\n'
        format_end_spacement  ='    # =================== #\n'
        
        if self.is_nginx_blank_config():
            self.create_default_nginx_config()

        try:
            with open(self.NGINX_CONF_PATH, 'r') as conf_file:
                content = conf_file.readlines()

            http_block_end_index = None
            for i, line in enumerate(content[::-1]):  # Procura de trás para frente
                if '}' in line:
                    http_block_end_index = len(content) - i - 1  # Calcula o índice correto
                    break

            if http_block_end_index is not None:
                # Insere o novo conteúdo antes do último fechamento de bloco '}'
                new_content = content[:http_block_end_index] + [
                    format_init_spacement,
                    "    #  Nginx DMtools Init  #\n",
                    f'{format_init_spacement}\n',
                    config_content + '\n',
                    f'\n{format_end_spacement}',
                    "    #  Nginx DMtools End  #\n",
                    f'{format_end_spacement}\n',
                ] + content[http_block_end_index:]
                
                # Sobrescreve o arquivo com o conteúdo atualizado
                with open(self.NGINX_CONF_PATH, 'w') as conf_file:
                    conf_file.writelines(new_content)

                if not noconsole or self.CONSOLE_OUT_ALL:
                    print(f"Configuração personalizada adicionada com sucesso ao arquivo '{os.path.basename(self.NGINX_CONF_PATH)}' no Windows.")
        except IOError as e:
            print(f"Erro ao modificar a configuração '{os.path.basename(self.NGINX_CONF_PATH)}' no Windows: {e}")

    def create_default_nginx_config(self):
        """
        Cria uma configuração padrão para o servidor NGINX no Windows, caso nenhuma configuração personalizada seja fornecida.
        
        Parâmetros:
        -----------
        - Nenhum
        
        Retorno:
        --------
        - None
        """
        try:
            with open(self.NGINX_CONF_PATH, 'r+') as conf_file:
                conf_file.write(NGINX_WIN_DEFAULT)

        except IOError as e:
            print(f"Erro ao modificar a configuração '{os.path.basename(self.NGINX_CONF_PATH)}' no Windows: {e}")
            
    def is_nginx_default_config(self):
        """
        Verifica se o arquivo de configuração do NGINX no Windows corresponde à configuração padrão.
        
        Parâmetros:
        -----------
        - Nenhum
        
        Retorno:
        --------
        - bool
            - Retorna True se o arquivo de configuração atual é o padrão, False caso contrário.
        """
        return self.is_actual_Config_iquals_expected(NGINX_WIN_DEFAULT, self.NGINX_CONF_PATH)

    def setup_nginx(self, directives=DEFAULT_DIRECTIVES_EX1, config_content=DEFAULT_NGINX_CONTENT_EX1, noconsole=True):  
        """
        Configura o servidor NGINX no Windows com diretivas específicas, substituindo ou atualizando a configuração existente.
        
        Parâmetros:
        -----------
        - directives : dict
            - Dicionário contendo as diretivas de configuração do NGINX e seus respectivos valores.
        - config_content : str
            - Conteúdo de configuração para ser escrito no arquivo nginx.conf.
        - noconsole : bool, opcional
            - Define se as mensagens de console durante a configuração devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """
        # MODIFY
        # AQUI Estou setando o create, mas é necessario fazer a tratativa caso o usuario tenha configs no nginx

        if not self.is_nginx_configured(directives):
            if not noconsole or self.CONSOLE_OUT_ALL:
                print("\nConfigurando servidor de proxy reverso...")
                
            if nginx_controller.is_nginx_blank_config():
                self.create_nginx_config(config_content)
                
            elif self.is_nginx_default_config():
                self.create_nginx_config(config_content)
            
            elif not all(index is not None for index in self.find_tag_indices()):
                self.create_nginx_config(config_content)
                
            else:
                self.update_nginx_config(config_content)
            
            self.stop_nginx()
            
            if not noconsole or self.CONSOLE_OUT_ALL:
                print("Servidor de proxy reverso configurado com sucesso.")
        
        self.start_nginx()

    def update_nginx_config(self, config_content=DEFAULT_NGINX_CONTENT_EX1, noconsole=True):
        """
        Atualiza a configuração do servidor NGINX no Windows com novo conteúdo, mantendo configurações personalizadas existentes.
        
        Parâmetros:
        -----------
        - config_content : str
            - Novo conteúdo de configuração para ser adicionado ou atualizado no arquivo nginx.conf.
        - noconsole : bool, opcional
            - Define se as mensagens de console durante a atualização devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """
        format_init_spacement ='    # ==================== #\n'
        format_end_spacement  ='    # =================== #\n'
        start_index, end_index = self.find_tag_indices()

        if start_index is not None and end_index is not None:
            try:
                with open(self.NGINX_CONF_PATH, 'r') as conf_file:
                    content_lines = conf_file.readlines()

                updated_content = content_lines[:start_index + 1] + [format_init_spacement] + ['\n'] + [config_content] + ['\n'*2] + [format_end_spacement] + content_lines[end_index:]
                # Sobrescrever arquivo com novo conteúdo
                with open(self.NGINX_CONF_PATH, 'w') as conf_file:
                    conf_file.writelines(updated_content)

                if not noconsole or self.CONSOLE_OUT_ALL:
                    print(f"Configuração personalizada atualizada com sucesso no arquivo '{os.path.basename(self.NGINX_CONF_PATH)}'.")
            except IOError as e:
                print(f"Erro ao modificar a configuração '{os.path.basename(self.NGINX_CONF_PATH)}': {e}")
        else:
            print("As tags de início e fim da configuração personalizada não foram encontradas.")

    def find_tag_indices(self, tag_init='#  Nginx DMtools Init  #', tag_end='#  Nginx DMtools End  #'):
        """
        Atualiza a configuração do servidor NGINX no Windows com novo conteúdo, mantendo configurações personalizadas existentes.
        
        Parâmetros:
        -----------
        - config_content : str
            - Novo conteúdo de configuração para ser adicionado ou atualizado no arquivo nginx.conf.
        - noconsole : bool, opcional
            - Define se as mensagens de console durante a atualização devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """
        try:
            with open(self.NGINX_CONF_PATH, 'r') as conf_file:
                content_lines = conf_file.readlines()

            start_index = None
            end_index = None

            # Encontrar índices das tags
            for i, line in enumerate(content_lines):
                if tag_init in line:
                    start_index = i
                elif tag_end in line:
                    end_index = i
                    break

            return start_index, end_index
        except IOError as e:
            print(f"Erro ao procurar as tags no arquivo '{os.path.basename(self.NGINX_CONF_PATH)}': {e}")
            return None, None

    def check_nginx_config(self, directives={}):
        """
        Verifica se as diretivas específicas estão presentes e corretamente configuradas no arquivo de configuração do NGINX no Windows.
        
        Parâmetros:
        -----------
        - directives : dict
            - Dicionário das diretivas de configuração para verificar, com suas respectivas regras de validação ou valores esperados.
            
        Retorno:
        --------
        - dict
            - Dicionário com os resultados das verificações para cada diretiva, indicando True para configurações corretas e False para incorretas.
        """
        nginx_conf_path = self.NGINX_CONF_PATH
        
        # Retorna um dicionário com os resultados das verificações para cada diretiva
        directive_results = {directive: False for directive in directives}
        
        if not os.path.exists(nginx_conf_path):
            print(f"O arquivo de configuração '{nginx_conf_path}' não foi encontrado.")
            return directive_results
        
        start_checking = False  # Flag para começar a verificar após encontrar a seção IP Redefiner

        try:
            with open(nginx_conf_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # Verifica se chegou na seção IP Redefiner
                    if '#  Nginx DMtools Init  #' in line:
                        start_checking = True
                        continue  # Pula para a próxima iteração para não processar a linha da seção
                    
                    if start_checking:
                        for directive, expected_value in directives.items():
                            if directive in line:
                                # Extrai o argumento da linha que contém a diretiva
                                match = re.search(rf'{directive}\s+([^;]+)', line)
                                if match:
                                    argument = match.group(1)
                                    # Verifica se o valor esperado é uma função de validação
                                    if callable(expected_value):
                                        directive_results[directive] = expected_value(argument)
                                    else:
                                        # Compara o argumento extraído com o valor esperado
                                        directive_results[directive] = (argument == expected_value)
                                        
                    if '#  Nginx DMtools End  #' in line:
                        break

                    
        except IOError as e:
            print(f"Erro ao ler o arquivo de configuração: {e}")
        
        return directive_results


    
class LinuxNginxController(NginxController):
    """
    Controla a configuração e gerenciamento do servidor NGINX em ambientes Linux.
    """
    NGINX_ROOT_PATH = '/etc/nginx'
    NGINX_CONF_PATH = os.path.join(NGINX_ROOT_PATH, 'sites-available')
    
    def start_nginx(self, noconsole=True):
        """
        Inicia o servidor NGINX utilizando o systemctl no Linux.

        Parâmetros:
        -----------
        - noconsole : bool, opcional
            - Define se as mensagens de console durante a inicialização devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """
        if self.is_nginx_running():
            return
        if not noconsole or self.CONSOLE_OUT_ALL:
            print("Iniciando servidor de proxy reverso...")
        nginx_command = 'systemctl start nginx'
        try:
            subprocess.run(nginx_command, shell=True, check=True)
            if not noconsole or self.CONSOLE_OUT_ALL:
                print("Servidor de proxy reverso iniciado com sucesso.")
        except subprocess.CalledProcessError as e:
            if not noconsole or self.CONSOLE_OUT_ALL:
                print(f"Erro ao iniciar o Nginx: {e}")

    def stop_nginx(self, noconsole=True):
        """
        Para o servidor NGINX utilizando o systemctl no Linux.

        Parâmetros:
        -----------
        - noconsole : bool, opcional
            - Define se as mensagens de console durante a parada devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """
        if not self.is_nginx_running():
            if not noconsole or self.CONSOLE_OUT_ALL:
                print("Nginx não está rodando.")
            return
        if not noconsole or self.CONSOLE_OUT_ALL:
            print("Encerrando servidor de proxy reverso...")
        nginx_command = 'systemctl stop nginx'
        try:
            subprocess.run(nginx_command, shell=True, check=True)
            if not noconsole or self.CONSOLE_OUT_ALL:
                print("Servidor de proxy reverso encerrado com sucesso")
        except subprocess.CalledProcessError as e:
            if not noconsole or self.CONSOLE_OUT_ALL:
                print(f"Erro ao encerrar o Nginx: {e}")

    def is_nginx_running(self):
        """
        Verifica se o servidor NGINX está em execução no Linux.

        Parâmetros:
        -----------
        - Nenhum
        
        Retorno:
        --------
        - bool
            - Retorna True se o NGINX estiver em execução, False caso contrário.
        """
        try:
            output = subprocess.check_output("pgrep nginx", shell=True)
            return bool(output)
        except subprocess.CalledProcessError:
            return False

    def is_nginx_blank_config(self, conf_name='default'):
        """
        Verifica se o arquivo de configuração do NGINX especificado está em branco no Linux.

        Parâmetros:
        -----------
        - conf_name : str, opcional
            - Nome do arquivo de configuração a ser verificado. Por padrão, é 'default'.
            
        Retorno:
        --------
        - bool
            - Retorna True se o arquivo de configuração estiver em branco, False caso contrário.
        """
        conf_path = os.path.join(self.NGINX_CONF_PATH, conf_name)
        try:
            with open(conf_path, 'r') as conf_file:
                content = conf_file.read().strip()
                return not content
        except FileNotFoundError:
            return True
        except Exception as e:
            print(f"Erro ao verificar o arquivo de configuração '{conf_name}': {e}")
            return False

    def create_nginx_config(self, conf_name='default', config_content=DEFAULT_NGINX_CONTENT_EX1, noconsole=True):
        """
        Cria ou atualiza um arquivo de configuração do NGINX com o conteúdo especificado no Linux.

        Parâmetros:
        -----------
        - conf_name : str
            - Nome do arquivo de configuração a ser criado ou atualizado.
        - config_content : str
            - Conteúdo de configuração para ser escrito no arquivo.
        - noconsole : bool, opcional
            - Define se as mensagens de console durante a criação ou atualização devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """
        conf_path = os.path.join(self.NGINX_CONF_PATH, conf_name)
        try:
            with open(conf_path, 'w') as conf_file:
                conf_file.write(config_content)
            if not noconsole or self.CONSOLE_OUT_ALL:
                print(f"Configuração personalizada adicionada com sucesso ao arquivo '{conf_name}' no Linux.")
        except IOError as e:
            print(f"Erro ao modificar a configuração '{conf_name}' no Linux: {e}")

    def create_default_nginx_config(self):
        """
        Cria uma configuração padrão para o servidor NGINX no Linux, caso nenhuma configuração personalizada seja fornecida.
        
        Parâmetros:
        -----------
        - Nenhum
        
        Retorno:
        --------
        - None
        """
        try:
            with open(self.NGINX_CONF_PATH, 'r+') as conf_file:
                conf_file.write(NGINX_WIN_DEFAULT)

        except IOError as e:
            print(f"Erro ao modificar a configuração '{os.path.basename(self.NGINX_CONF_PATH)}' no Linux: {e}")

    def is_nginx_default_config(self, conf_name='default'):
        """
        Verifica se o arquivo de configuração do NGINX no Linux corresponde à configuração padrão.
        
        Parâmetros:
        -----------
        - conf_name : str, opcional
            - Nome do arquivo de configuração a ser verificado. Por padrão, é 'default'.
            
        Retorno:
        --------
        - bool
            - Retorna True se o arquivo de configuração atual é o padrão, False caso contrário.
        """        
        return self.is_actual_Config_iquals_expected(NGINX_WIN_DEFAULT, os.path.join(nginx_controller.NGINX_CONF_PATH, conf_name))

    def setup_nginx(self, directives=DEFAULT_DIRECTIVES_EX1, config_content=DEFAULT_NGINX_CONTENT_EX1, noconsole=True):
        """
        Configura o servidor NGINX no Linux com diretivas específicas, substituindo ou atualizando a configuração existente.
        
        Parâmetros:
        -----------
        - directives : dict
            - Dicionário contendo as diretivas de configuração do NGINX e seus respectivos valores.
        - config_content : str
            - Conteúdo de configuração para ser escrito no arquivo nginx.conf.
        - noconsole : bool, opcional
            - Define se as mensagens de console durante a configuração devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """        
        # MODIFY
        # AQUI Estou setando o create, mas é necessario fazer a tratativa caso o usuario tenha configs no nginx

        if not self.is_nginx_configured(directives):
            if not noconsole or self.CONSOLE_OUT_ALL:
                print("\nConfigurando servidor de proxy reverso...")
                
            if nginx_controller.is_nginx_blank_config():
                self.create_nginx_config(config_content)
                
            elif self.is_nginx_default_config():
                self.create_nginx_config(config_content)
            
            elif not all(index is not None for index in self.find_tag_indices()):
                self.create_nginx_config(config_content)
                
            else:
                self.update_nginx_config(config_content)
            
            self.stop_nginx()
            
            if not noconsole or self.CONSOLE_OUT_ALL:
                print("Servidor de proxy reverso configurado com sucesso.")
        
        self.start_nginx()

    def update_nginx_config(self, config_content=DEFAULT_NGINX_CONTENT_EX1, noconsole=True):
        """
        Atualiza a configuração do servidor NGINX no Linux com novo conteúdo, mantendo configurações personalizadas existentes.
        
        Parâmetros:
        -----------
        - config_content : str
            - Novo conteúdo de configuração para ser adicionado ou atualizado no arquivo nginx.conf.
        - noconsole : bool, opcional
            - Define se as mensagens de console durante a atualização devem ser suprimidas. Por padrão, é True.
            
        Retorno:
        --------
        - None
        """        
        format_init_spacement ='    # ==================== #\n'
        format_end_spacement  ='    # =================== #\n'
        start_index, end_index = self.find_tag_indices()

        if start_index is not None and end_index is not None:
            try:
                with open(self.NGINX_CONF_PATH, 'r') as conf_file:
                    content_lines = conf_file.readlines()

                updated_content = content_lines[:start_index + 1] + [format_init_spacement] + ['\n'] + [config_content] + ['\n'*2] + [format_end_spacement] + content_lines[end_index:]
                # Sobrescrever arquivo com novo conteúdo
                with open(self.NGINX_CONF_PATH, 'w') as conf_file:
                    conf_file.writelines(updated_content)

                if not noconsole or self.CONSOLE_OUT_ALL:
                    print(f"Configuração personalizada atualizada com sucesso no arquivo '{os.path.basename(self.NGINX_CONF_PATH)}'.")
            except IOError as e:
                print(f"Erro ao modificar a configuração '{os.path.basename(self.NGINX_CONF_PATH)}': {e}")
        else:
            print("As tags de início e fim da configuração personalizada não foram encontradas.")
        
    def find_tag_indices(self, tag_init='#  Nginx DMtools Init  #', tag_end='#  Nginx DMtools End  #'):
        """
        Localiza os índices de início e fim de uma configuração personalizada dentro do arquivo de configuração do NGINX no Linux.
        
        Parâmetros:
        -----------
        - tag_init : str
            - Tag que marca o início da configuração personalizada.
        - tag_end : str
            - Tag que marca o fim da configuração personalizada.
            
        Retorno:
        --------
        - tuple
            - Retorna um par (start_index, end_index) representando os índices das tags de início e fim. Retorna (None, None) se alguma das tags não for encontrada.
        """
        try:
            with open(self.NGINX_CONF_PATH, 'r') as conf_file:
                content_lines = conf_file.readlines()

            start_index = None
            end_index = None

            # Encontrar índices das tags
            for i, line in enumerate(content_lines):
                if tag_init in line:
                    start_index = i
                elif tag_end in line:
                    end_index = i
                    break

            return start_index, end_index
        except IOError as e:
            print(f"Erro ao procurar as tags no arquivo '{os.path.basename(self.NGINX_CONF_PATH)}': {e}")
            return None, None

    def check_nginx_config(self, directives={}):
        """
        Verifica se as diretivas específicas estão presentes e corretamente configuradas no arquivo de configuração do NGINX no Linux.
        
        Parâmetros:
        -----------
        - directives : dict
            - Dicionário das diretivas de configuração para verificar, com suas respectivas regras de validação ou valores esperados.
            
        Retorno:
        --------
        - dict
            - Dicionário com os resultados das verificações para cada diretiva, indicando True para configurações corretas e False para incorretas.
        """        
        nginx_conf_path = self.NGINX_CONF_PATH
        
        # Retorna um dicionário com os resultados das verificações para cada diretiva
        directive_results = {directive: False for directive in directives}
        
        if not os.path.exists(nginx_conf_path):
            print(f"O arquivo de configuração '{nginx_conf_path}' não foi encontrado.")
            return directive_results
        
        start_checking = False  # Flag para começar a verificar após encontrar a seção IP Redefiner

        try:
            with open(nginx_conf_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # Verifica se chegou na seção IP Redefiner
                    if '#  Nginx DMtools Init  #' in line:
                        start_checking = True
                        continue  # Pula para a próxima iteração para não processar a linha da seção
                    
                    if start_checking:
                        for directive, expected_value in directives.items():
                            if directive in line:
                                # Extrai o argumento da linha que contém a diretiva
                                match = re.search(rf'{directive}\s+([^;]+)', line)
                                if match:
                                    argument = match.group(1)
                                    # Verifica se o valor esperado é uma função de validação
                                    if callable(expected_value):
                                        directive_results[directive] = expected_value(argument)
                                    else:
                                        # Compara o argumento extraído com o valor esperado
                                        directive_results[directive] = (argument == expected_value)
                                        
                    if '#  Nginx DMtools End  #' in line:
                        break

                    
        except IOError as e:
            print(f"Erro ao ler o arquivo de configuração: {e}")
        
        return directive_results


    
    
if platform.system() == 'Windows':
    nginx_controller = WindowsNginxController()
else:
    nginx_controller = LinuxNginxController()



if __name__ == '__main__':
    nginx_controller.setup_nginx(DEFAULT_DIRECTIVES_IP, DEFAULT_NGINX_CONTENT_IP)
    
    # nginx_controller.stop_nginx()
    
    
    pass