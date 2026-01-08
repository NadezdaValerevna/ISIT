"""
Семантическая сеть знаний об архетипах личности
"""

class Node:
    """Узел семантической сети"""
    def __init__(self, name: str, type: str, **attrs):
        self.name = name
        self.type = type
        self.attrs = attrs
        self.links = {}  # тип_связи -> [узлы]

    def link(self, rel_type: str, target):
        """Добавляет связь"""
        if rel_type not in self.links:
            self.links[rel_type] = []
        self.links[rel_type].append(target)

    def __repr__(self):
        return f"{self.name}({self.type})"

class SemanticNetwork:
    """Семантическая сеть"""

    def __init__(self):
        self.nodes = {}
        self._build()

    def _build(self):
        """Строит сеть знаний"""
        # Архетипы
        archetypes = {
            "АРХИТЕКТОР": {"desc": "Аналитичный, ориентированный на детали", "reason": "Выбрали планирование и внимание к деталям"},
            "СТРАТЕГ": {"desc": "Видит общую картину, стратег", "reason": "Выбрали планирование, но предпочитаете общую картину"},
            "ЛИДЕР": {"desc": "Прирожденный руководитель", "reason": "Выбрали действие и лидерство"},
            "ВОИН": {"desc": "Целеустремленный исполнитель", "reason": "Выбрали действие и целеустремленность"},
            "ОПЕКУН": {"desc": "Эмпатичный, заботливый", "reason": "Выбрали сотрудничество и эмпатию"},
            "МИРОТВОРЕЦ": {"desc": "Дипломатичный, гармония", "reason": "Выбрали сотрудничество и дипломатичность"},
            "ТВОРЕЦ": {"desc": "Творческий, воображение", "reason": "Выбрали творчество и воображение"},
            "ПРОВИДЕЦ": {"desc": "Интуитивный, проницательный", "reason": "Выбрали творчество и интуицию"}
        }

        # Добавляем узлы
        for name, attrs in archetypes.items():
            self.nodes[name] = Node(name, "archetype", **attrs)

        # Вопросы
        questions = [
            ("q1", "Для вас справедливость важнее гармонии?", "justice"),
            ("q2_plan", "Вы предпочитаете планирование?", "planning"),
            ("q2_coop", "Вы предпочитаете сотрудничество?", "cooperation"),
            ("q3_detail", "Вы ориентированы на детали?", "detail"),
            ("q3_leader", "Вы прирожденный лидер?", "leader"),
            ("q3_empathy", "У вас глубокая эмпатия?", "empathy"),
            ("q3_imagine", "У вас богатое воображение?", "imagination")
        ]

        for qid, text, var in questions:
            self.nodes[qid] = Node(qid, "question", text=text, var=var)

        # Строим связи
        # Дерево решений
        self.nodes["q1"].link("yes", self.nodes["q2_plan"])
        self.nodes["q1"].link("no", self.nodes["q2_coop"])

        self.nodes["q2_plan"].link("yes", self.nodes["q3_detail"])
        self.nodes["q2_plan"].link("no", self.nodes["q3_leader"])

        self.nodes["q2_coop"].link("yes", self.nodes["q3_empathy"])
        self.nodes["q2_coop"].link("no", self.nodes["q3_imagine"])

        # Связи с архетипами
        self.nodes["q3_detail"].link("yes", self.nodes["АРХИТЕКТОР"])
        self.nodes["q3_detail"].link("no", self.nodes["СТРАТЕГ"])

        self.nodes["q3_leader"].link("yes", self.nodes["ЛИДЕР"])
        self.nodes["q3_leader"].link("no", self.nodes["ВОИН"])

        self.nodes["q3_empathy"].link("yes", self.nodes["ОПЕКУН"])
        self.nodes["q3_empathy"].link("no", self.nodes["МИРОТВОРЕЦ"])

        self.nodes["q3_imagine"].link("yes", self.nodes["ТВОРЕЦ"])
        self.nodes["q3_imagine"].link("no", self.nodes["ПРОВИДЕЦ"])

        # Добавляем описания для промежуточных узлов
        self.nodes["justice"] = Node("justice", "value", desc="Ориентация на справедливость или гармонию")
        self.nodes["planning"] = Node("planning", "value", desc="Предпочтение планирования")
        self.nodes["action"] = Node("action", "value", desc="Предпочтение действия")
        self.nodes["cooperation"] = Node("cooperation", "value", desc="Предпочтение сотрудничества")
        self.nodes["creativity"] = Node("creativity", "value", desc="Предпочтение творчества")

    def get_node(self, name):
        """Возвращает узел по имени"""
        return self.nodes.get(name)