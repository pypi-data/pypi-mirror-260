from setuptools import setup, find_packages

# Carregando a descrição longa do README.md
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dmtoolbox-win',
    version='0.1.1',
    packages=find_packages(),
    description='Uma extensão do dmtoolbox focada em funcionalidades específicas do Windows, incluindo manipulação de registros, criação de executáveis e gerenciamento de arquivos e configurações avançadas do sistema.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel Mello',
    author_email='danielmello.dev@gmail.com',
    license='GPLv3',
    install_requires=[
        'pyinstaller>=6.4.0',
        'pefile>=2023.2.7',
        'dmtoolbox>=0.1.22'
    ],
    python_requires='>=3.6',
    url='https://github.com/DanielMelloo/dmtoolbox-win',
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

