from setuptools import setup, find_packages
import os

with open ("README.md", "r") as file:
    LONG_DESCRIPTION= file.read()

install_require = []
if os.name == 'nt':
    install_require.append('windows-curses')

VERSION = '0.0.1'
DESCRIPTION = 'A simple terminal-based typing test'

setup(
    name="terminaltype",
    version=VERSION,
    author="Ramiro Cabral",
    author_email="<ramiro.cabral@alu.ing.unlp.edu.ar>",
    url="https://github.com/ramirocabral/terminaltype",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'typing', 'test', 'game', 'curses'],
    install_requires=install_require,
    extras_require={
        'dev': ["twine>=4.0.2"]
    },
    python_requires='>=3.10',
    license="GPL",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={
        "console_scripts": [
            "terminaltype=terminaltype.app:App",
        ],
    },

)
