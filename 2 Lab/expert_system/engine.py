"""Основной движок правил - переносим RuleEngine сюда."""

import json
from typing import Any, Dict, List
from memory import Memory  # новый модуль
from expert_system.actions import ActionHandler  # новый модуль


class RuleEngine:
    def __init__(self, rules_file: str = 'lab.json'):
        with open(rules_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Используем модуль памяти
        self.memory = Memory(
            rules=data['rules'],
            questions=data['questions'],
            initial_facts=data['initial_facts'].copy(),
            mbti_mapping=data.get('mbti_mapping', {})
        )

        # Используем модуль обработки действий
        self.actions = ActionHandler(self.memory)

    def ask(self, qid: str) -> Any:
        """Задает вопрос пользователю."""
        return self.memory.ask_question(qid)

    def check_condition(self, cond: Dict) -> bool:
        """Проверяет одно условие."""
        fact = self.memory.facts.get(cond['fact'])

        if 'exists' in cond:
            return (fact is not None) if cond['exists'] else (fact is None)

        if fact is None:
            return False

        if 'operator' not in cond:
            expected = cond['value']
            if isinstance(expected, list):
                return fact in expected
            return fact == expected

        op = cond['operator']
        expected = cond['value']

        if op == '>': return fact > expected
        if op == '>=': return fact >= expected
        if op == '<': return fact < expected
        if op == '<=': return fact <= expected
        return False

    def check_all(self, conditions: List[Dict]) -> bool:
        """Проверяет все условия."""
        return all(self.check_condition(c) for c in conditions)

    def execute_action(self, action: Dict):
        """Выполняет одно действие через ActionHandler."""
        self.actions.execute(action)

    def run_cycle(self) -> bool:
        """Выполняет один цикл активации правил."""
        activated = []
        for rule in self.memory.rules:
            if self.check_all(rule['conditions']):
                activated.append(rule)

        if not activated:
            return False

        # СТРАТЕГИЯ ПО ПОРЯДКУ: выполняем правила как есть, без сортировки
        for rule in activated:
            for action in rule['actions']:
                self.execute_action(action)

        return True

    def run(self):
        """Основной цикл выполнения системы."""
        print("\n" + "=" * 50)
        print("Экспертная система: Анализ личности")
        print("=" * 50)

        cycle = 0
        while cycle < 50:
            cycle += 1

            # Проверяем, все ли данные собраны
            if self.memory.facts.get('all_data_collected'):
                # Запускаем еще несколько циклов для обработки рекомендаций
                for _ in range(5):
                    self.run_cycle()
                break

            if not self.run_cycle():
                # Прямой опрос
                for rule in self.memory.rules:
                    for action in rule.get('actions', []):
                        if action['type'] == 'ask_user':
                            qid = action['question']
                            fact = action['fact']
                            if qid not in self.memory.asked and self.memory.facts.get(fact) is None:
                                ans = self.ask(qid)
                                self.memory.facts[fact] = ans
                                self.memory.asked.add(qid)
                                break
                    else:
                        continue
                    break
                else:
                    # Больше нет вопросов
                    break

        # Вывод результатов
        self.memory.print_results()