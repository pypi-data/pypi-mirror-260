from setuptools import setup, find_packages

# Carregando a descrição longa do README.md
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dmtoolbox',
    version='0.1.1',
    packages=find_packages(),
    description='dmtoolbox é uma coleção abrangente de ferramentas Python projetadas para facilitar a automação de tarefas e operações no ambiente Windows, manipulação avançada de arquivos e diretórios, criação e gestão de executáveis, manipulação de dados JSON, gerenciamento de configurações NGINX, análise numérica, e muito mais.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel Mello',
    author_email='danielmello.dev@gmail.com',
    license='GPLv3',
    install_requires=[
        'pandas==2.2.1',
        'numpy==1.26.4',
        'prettytable==3.10.0',
        'matplotlib==3.8.3',
        'colorama==0.4.6',
        'pyinstaller==6.4.0',
        'openpyxl==3.1.2',
    ],
    python_requires='>=3.6',
    url='https://github.com/danielmello/dmtoolbox',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='utils automation numpy pandas matplotlib',
)

