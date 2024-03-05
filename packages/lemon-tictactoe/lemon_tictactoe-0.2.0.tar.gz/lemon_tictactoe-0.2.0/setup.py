from setuptools import setup, find_packages

setup(
    name="lemon_tictactoe",
    version="0.2.0",
    packages=find_packages(),
    license="GNU General Public License v3.0",
    description="A library simplifying the process of embedding a TicTacToe game in your python project.",
    author="Zitronenjoghurt",
    extras_require={'dev': ['pytest']},
    url="https://github.com/Zitronenjoghurt/Lemon-TicTacToe"
)