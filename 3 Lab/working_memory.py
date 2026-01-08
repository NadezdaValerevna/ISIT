"""
Рабочая память для хранения фактов
"""

class WorkingMemory:
    """Рабочая память системы"""

    def __init__(self):
        self.facts = {}
        self.history = []
        self.reasoning_chain = []

    def assert_fact(self, variable, value, reason=None):
        """Добавляет факт с обоснованием"""
        self.facts[variable] = value
        self.history.append((variable, value))
        if reason:
            self.reasoning_chain.append(reason)

    def retract_fact(self, variable):
        """Удаляет факт"""
        if variable in self.facts:
            del self.facts[variable]

    def get_fact(self, variable):
        """Получает значение факта"""
        return self.facts.get(variable)

    def has_fact(self, variable):
        """Проверяет наличие факта"""
        return variable in self.facts

    def clear(self):
        """Очищает память"""
        self.facts.clear()
        self.history.clear()
        self.reasoning_chain.clear()

    def get_all_facts(self):
        """Возвращает все факты"""
        return dict(self.facts)

    def get_reasoning_chain(self):
        """Возвращает цепочку рассуждений"""
        return list(self.reasoning_chain)