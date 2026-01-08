"""
Главный модуль системы определения архетипов личности
"""

from semantic_network import SemanticNetwork
from working_memory import WorkingMemory
from inference_engine import InferenceEngine
from interface import Interface


def main():
    """Основная функция"""
    # Инициализация компонентов
    network = SemanticNetwork()
    memory = WorkingMemory()
    engine = InferenceEngine(network, memory)
    ui = Interface(engine)

    # Запуск системы
    ui.run()


if __name__ == "__main__":
    main()