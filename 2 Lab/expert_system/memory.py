"""Модуль для работы с памятью и выводом результатов."""

from typing import Any, Dict


class Memory:
    """Управление памятью системы."""

    def __init__(self, rules, questions, initial_facts, mbti_mapping):
        self.rules = rules
        self.questions = questions
        self.facts = initial_facts
        self.mbti_map = mbti_mapping
        self.asked = set()

    def ask_question(self, qid: str) -> Any:
        """Задает вопрос пользователю."""
        q = self.questions[qid]
        print(f"\n{q['text']}")

        if 'explanation' in q:
            print(f"({q['explanation']})")

        if q['type'] == 'boolean':
            while True:
                ans = input("(да/нет): ").lower()
                if ans in ['да', 'д', 'yes', 'y', '1']:
                    return True
                elif ans in ['нет', 'н', 'no', 'n', '0']:
                    return False

        elif q['type'] == 'integer':
            while True:
                try:
                    val = int(input("Введите число: "))
                    if 'validation' in q:
                        if q['validation'] == 'min_0' and val < 0:
                            print("Должно быть >= 0")
                            continue
                        if q['validation'] == 'range_1_5' and not (1 <= val <= 5):
                            print("Должно быть от 1 до 5")
                            continue
                    return val
                except:
                    print("Введите целое число")

        elif q['type'] == 'choice':
            print(f"Варианты: {', '.join(q['options'])}")
            while True:
                ans = input("Ваш выбор: ")
                if ans in q['options']:
                    return ans

    def print_results(self):
        """Выводит результаты анализа."""
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ АНАЛИЗА")
        print("=" * 50)

        if 'mbti_type' in self.facts:
            print(f"\n ТИП ЛИЧНОСТИ: {self.facts['mbti_type']}")

        if 'diagnosis' in self.facts:
            print(f"\n ОПИСАНИЕ:\n{self.facts['diagnosis']}")

        # Анализ Big Five
        big5_found = False
        for key, label in [
            ('extraversion_analysis', 'Экстраверсия'),
            ('openness_analysis', 'Открытость'),
            ('conscientiousness_analysis', 'Добросовестность'),
            ('emotional_analysis', 'Эмоциональная стабильность')
        ]:
            if key in self.facts:
                if not big5_found:
                    print(f"\n ЧЕРТЫ ЛИЧНОСТИ:")
                    big5_found = True
                print(f"  • {label}: {self.facts[key]}")

        # Рекомендации
        if 'career_recommendation' in self.facts:
            print(f"\n КАРЬЕРА:\n{self.facts['career_recommendation']}")

        if 'communication_recommendation' in self.facts:
            print(f"\n  ОБЩЕНИЕ:\n{self.facts['communication_recommendation']}")

        if 'growth_recommendation' in self.facts:
            print(f"\n РАЗВИТИЕ:\n{self.facts['growth_recommendation']}")

        if 'integrated_report' in self.facts:
            print(f"\n ПОЛНЫЙ ОТЧЕТ:\n{self.facts['integrated_report']}")