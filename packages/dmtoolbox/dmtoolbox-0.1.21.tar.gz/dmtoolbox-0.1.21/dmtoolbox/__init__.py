from .appdataGen import *
from .createExeOnC import *
from .func import *
from .genJsons import *
from .nginxDefaults import *
from .nginxUtils import *
from .numericFuncs import *
from .osFuncs import *
from .portTools import *

# Definição de __all__ para exportar corretamente os símbolos de cada módulo
__all__ = (appdataGen.__all__ +
           createExeOnC.__all__ +
           func.__all__ +
           genJsons.__all__ +
           nginxDefaults.__all__ +
           nginxUtils.__all__ +
           numericFuncs.__all__ +
           osFuncs.__all__ +
           portTools.__all__)


# system_plat = platform.system()
    
# if system_plat == 'Windows':
#     try:            
#         from .exeGenerator import *
#         __all__ += exeGenerator.__all__
        
#         from .regedit import *
#         __all__ += regedit.__all__
#     except ImportError as e:
#         print('Dependência necessária não encontrada:', e)
#         print('Tentando instalar dependências específicas do Windows...')
  
#         # Tenta importar novamente após a instalação
#         from .exeGenerator import *
#         __all__ += exeGenerator.__all__
        
#         from .regedit import *
#         __all__ += regedit.__all__
# else:
#     print('Algumas funcionalidades específicas do Windows não estão disponíveis.')



