"""
main.py

Esse módulo apresenta a implementação da main, que inicializa e executa todo o código para funcionamento do programa.
"""

from controller import Controller

# Executa somente se esse programa é chamado diretamente na compilação
if __name__ == "__main__":

    controller = Controller()

    controller.start()

