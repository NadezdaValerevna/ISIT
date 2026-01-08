"""
Движок вывода на семантической сети
"""

class InferenceEngine:
    """Механизм логического вывода"""

    def __init__(self, network, memory):
        self.network = network
        self.memory = memory

    def infer_next_question(self):
        """Определяет следующий вопрос"""
        if not self.memory.has_fact("justice"):
            return self.network.get_node("q1")

        justice = self.memory.get_fact("justice")

        if justice == "yes":
            if not self.memory.has_fact("planning"):
                return self.network.get_node("q2_plan")

            planning = self.memory.get_fact("planning")
            if planning == "yes" and not self.memory.has_fact("detail"):
                return self.network.get_node("q3_detail")
            elif planning == "no" and not self.memory.has_fact("leader"):
                return self.network.get_node("q3_leader")

        else:  # justice == "no"
            if not self.memory.has_fact("cooperation"):
                return self.network.get_node("q2_coop")

            coop = self.memory.get_fact("cooperation")
            if coop == "yes" and not self.memory.has_fact("empathy"):
                return self.network.get_node("q3_empathy")
            elif coop == "no" and not self.memory.has_fact("imagination"):
                return self.network.get_node("q3_imagine")

        return None

    def get_answer_reasoning(self, question_node, answer):
        """Получает обоснование для ответа"""
        var_name = question_node.attrs["var"]
        answer_map = {
            "justice": {
                "yes": "Вы выбрали приоритет справедливости над гармонией",
                "no": "Вы выбрали приоритет гармонии над справедливостью"
            },
            "planning": {
                "yes": "Вы предпочитаете тщательное планирование",
                "no": "Вы предпочитаете немедленные действия"
            },
            "cooperation": {
                "yes": "Вы предпочитаете сотрудничество",
                "no": "Вы предпочитаете творческие решения"
            },
            "detail": {
                "yes": "Вы ориентированы на детали",
                "no": "Вы видите общую картину"
            },
            "leader": {
                "yes": "Вы прирожденный лидер",
                "no": "Вы целеустремленный исполнитель"
            },
            "empathy": {
                "yes": "У вас глубокая эмпатия",
                "no": "У вас дипломатические навыки"
            },
            "imagination": {
                "yes": "У вас богатое воображение",
                "no": "У вас сильная интуиция"
            }
        }

        return answer_map.get(var_name, {}).get(answer, "")

    def get_intermediate_conclusions(self):
        """Получает промежуточные выводы"""
        conclusions = []
        facts = self.memory.get_all_facts()

        if "justice" in facts:
            if facts["justice"] == "yes":
                if "planning" in facts:
                    if facts["planning"] == "yes":
                        conclusions.append("→ Вы на ветви 'Справедливость' с подходом 'Планирование'")
                    else:
                        conclusions.append("→ Вы на ветви 'Справедливость' с подходом 'Действие'")
            else:
                if "cooperation" in facts:
                    if facts["cooperation"] == "yes":
                        conclusions.append("→ Вы на ветви 'Гармония' с подходом 'Сотрудничество'")
                    else:
                        conclusions.append("→ Вы на ветви 'Гармония' с подходом 'Творчество'")

        return conclusions

    def process_answer(self, question_node, answer):
        """Обрабатывает ответ на вопрос"""
        var_name = question_node.attrs["var"]
        reasoning = self.get_answer_reasoning(question_node, answer)

        if reasoning:
            self.memory.assert_fact(var_name, answer, reasoning)
        else:
            self.memory.assert_fact(var_name, answer)

        # Добавляем промежуточные выводы
        conclusions = self.get_intermediate_conclusions()
        for conclusion in conclusions:
            if conclusion not in self.memory.reasoning_chain:
                self.memory.reasoning_chain.append(conclusion)

        # Проверяем, можно ли определить архетип
        return self.infer_archetype()

    def infer_archetype(self):
        """Определяет архетип на основе фактов"""
        if not self.memory.has_fact("justice"):
            return None

        justice = self.memory.get_fact("justice")

        if justice == "yes":
            if not self.memory.has_fact("planning"):
                return None
            planning = self.memory.get_fact("planning")

            if planning == "yes":
                if not self.memory.has_fact("detail"):
                    return None
                detail = self.memory.get_fact("detail")
                return "АРХИТЕКТОР" if detail == "yes" else "СТРАТЕГ"
            else:
                if not self.memory.has_fact("leader"):
                    return None
                leader = self.memory.get_fact("leader")
                return "ЛИДЕР" if leader == "yes" else "ВОИН"

        else:  # justice == "no"
            if not self.memory.has_fact("cooperation"):
                return None
            coop = self.memory.get_fact("cooperation")

            if coop == "yes":
                if not self.memory.has_fact("empathy"):
                    return None
                empathy = self.memory.get_fact("empathy")
                return "ОПЕКУН" if empathy == "yes" else "МИРОТВОРЕЦ"
            else:
                if not self.memory.has_fact("imagination"):
                    return None
                imagine = self.memory.get_fact("imagination")
                return "ТВОРЕЦ" if imagine == "yes" else "ПРОВИДЕЦ"

        return None