from setuptools import setup, find_packages

with open('README_pypi.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="lemon_tictactoe",
    python_requires=">=3.9",
    version="0.2.2",
    packages=find_packages(),
    license="GNU General Public License v3.0",
    description="A library simplifying the process of embedding a TicTacToe game in your python project.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Zitronenjoghurt",
    extras_require={'dev': ['pytest', 'twine', 'wheel']},
    url="https://github.com/Zitronenjoghurt/Lemon-TicTacToe"
)